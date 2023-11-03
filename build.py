import yaml
import frontmatter
import logging
import os
import jinja2
import markdown
import shutil
from jinja2 import Environment, FileSystemLoader


env = Environment(loader=FileSystemLoader("./src"))

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="build.log",
)

logger = logging.getLogger("website")

# Some Paths
data_path = "./src/_site/data.yaml"
posts_path = "./src/_posts"
src = "./src"
home_path = "./src/_site/home.md"
about_path = "./src/_site/about.md"

# Read the data.yaml
site_config = None
try:
    with open(data_path, "r") as file:
        site_config = yaml.safe_load(file)
        author = site_config["author"]
        email = site_config["email"]
        twitter = site_config["twitter"]
        github = site_config["github"]
        logger.debug("Data.yaml successfully loaded")
except Exception as e:
    logger.error("Failed to load data.yaml: %s", str(e))

# Get all the posts into an array
posts = []
try:
    for filename in os.listdir(posts_path):
        if filename.endswith(".md"):  # Assuming your posts are Markdown files
            post_path = os.path.join(posts_path, filename)
            with open(post_path, "r") as post_file:
                posts.append({post_path: frontmatter.load(post_file)})
    logger.debug("Posts successfully loaded")
except Exception as e:
    logger.error("Failed to load the posts from _posts: %s", str(e))

# Get Home Page
home = None
try:
    home = frontmatter.load(home_path)
    logger.debug("home.md successfully loaded")
except Exception as e:
    logger.error("Failed to load home.md: %s", str(e))

# Get About Page
about = None
try:
    about = frontmatter.load(about_path)
    logger.debug("about.md successfully loaded")
except Exception as e:
    logger.error("Failed to load about.md: %s", str(e))

# Copy js folder to dist
shutil.copytree("./src/js", "./dist/js", dirs_exist_ok=True)

# Build index in dist
page_index = None
with open("./src/index.html", "r") as file:
    page_index = file.read()

template_index = env.from_string(page_index)
rendered_index = template_index.render()

with open("./dist/index.html", "w") as file:
    file.write(rendered_index)
with open("./dist/404.html", "w") as file:
    file.write(rendered_index)

# Build home in dist
page_home = None
with open("./src/home.html", "r") as file:
    page_home = file.read()

template_home = env.from_string(page_home)
rendered_home = template_home.render()

with open("./dist/home.html", "w") as file:
    file.write(rendered_home)


# Build about in dist
page_about = None
with open("./src/about.html", "r") as file:
    page_about = file.read()

template_about = env.from_string(page_about)
rendered_about = template_about.render()

with open("./dist/about.html", "w") as file:
    file.write(rendered_about)

# Build blog in dist
page_blog = None
post_keys = []
for i in posts:
    input_string = [a for a in i.keys()][0]
    post_keys.append(
        (
            input_string.split("/")[-1]
            .split(".md")[0]
            .split("-", 3)[-1]
            .replace("-", " "),
            "-".join(input_string.split("/")[-1].split(".md")[0].split("-")[:3][::-1]),
        )
    )
# print(post_keys)
post_data = [
    {
        "title": pk[0],
        "date": pk[1],
        "slug": pk[0].replace(" ", "_"),
    }
    for pk in post_keys
]

# print(post_data)

with open("./src/blog.html", "r") as file:
    page_blog = file.read()

template_blog = env.from_string(page_blog)
rendered_blog = template_blog.render(posts=post_data)

with open("./dist/blog.html", "w") as file:
    file.write(rendered_blog)

# Render home, about, blog into router.js in dist
page_router = None
with open("./src/js/router.js", "r") as file:
    page_router = file.read()

template_router = env.from_string(page_router)
rendered_router = template_router.render(
    home=markdown.markdown(home.content),
    about=markdown.markdown(about.content),
    blog=rendered_blog,
)

with open("./dist/js/router.js", "w") as file:
    file.write(rendered_router)

print("\nNo Build Errors!............\n")


# Copy dist folder to docs for github pages hosting
shutil.copytree("./dist", "./docs", dirs_exist_ok=True)
