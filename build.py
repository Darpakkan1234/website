import yaml
import frontmatter
import logging
import os
import markdown
import shutil
from jinja2 import Environment, FileSystemLoader
from flask import Flask, render_template, send_from_directory

# Initialize Flask app
app = Flask(__name__, template_folder=".", static_folder="./static")
app.root_path = app.root_path + "/docs"

# Initialize Jinja2 environment
env = Environment(loader=FileSystemLoader("./src"))

# Configure the logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="build.log",
)

logger = logging.getLogger("website")

docs_folder_path = "./docs"
# Check if the /docs folder exists
if os.path.exists(docs_folder_path):
    # Remove the /docs folder and its contents
    shutil.rmtree(docs_folder_path)
    logger.debug(f"The {docs_folder_path} directory has been deleted.")
else:
    logger.debug(f"The {docs_folder_path} directory does not exist.")

# Define file paths
data_path = "./src/_site/data.yaml"
posts_path = "./src/_posts"
src = "./src"
home_path = "./src/_site/home.md"
about_path = "./src/_site/about.md"

# Read data from data.yaml
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

# Copy static folders/files to docs
shutil.copytree("./src/static", "./docs/static", dirs_exist_ok=True)
logger.debug("static files copied to docs")

# Build index in docs
page_index = None
with open("./src/index.html", "r") as file:
    page_index = file.read()

template_index = env.from_string(page_index)
rendered_index = template_index.render(home=markdown.markdown(home.content))

with open("./docs/index.html", "w") as file:
    file.write(rendered_index)
    logger.debug("index.html successfully built and saved")

with open("./docs/404.html", "w") as file:
    file.write(rendered_index)
    logger.debug("404.html successfully built and saved")

# Build about in docs
page_about = None
with open("./src/about.html", "r") as file:
    page_about = file.read()
    logger.debug("about.html content loaded")

template_about = env.from_string(page_about)
rendered_about = template_about.render(about=markdown.markdown(about.content))
logger.debug("about.html content rendered")

with open("./docs/about.html", "w") as file:
    file.write(rendered_about)
    logger.debug("about.html successfully built and saved")


# Build blog in docs
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
            input_string,
        )
    )

logger.debug("Post keys generated")


def get_postcontent(path):
    with open(path, "r") as file:
        return markdown.markdown(frontmatter.load(file).content)


post_data = [
    {
        "title": pk[0],
        "date": pk[1],
        "slug": pk[0].replace(" ", "-"),
        "content": get_postcontent(pk[2]),
    }
    for pk in post_keys
]

logger.debug("Post data generated")

with open("./src/blog.html", "r") as file:
    page_blog = file.read()
    logger.debug("blog.html content loaded")

template_blog = env.from_string(page_blog)
rendered_blog = template_blog.render(posts=post_data)

with open("./docs/blog.html", "w") as file:
    file.write(rendered_blog)
    logger.debug("blog.html successfully built and saved")

logger.info("No Build Errors!............")

# Build each post
with open("./src/post.html", "r") as file:
    page_post = file.read()
    template_post = env.from_string(page_post)

for post in post_data:
    rendered_post = template_post.render(post=post)
    post_slug = post["slug"]
    with open(f"./docs/{post_slug}.html", "w") as file:
        file.write(rendered_post)
        logger.debug(f"{post_slug}.html successfully built and saved")


# Start the dev server
@app.route("/")
@app.route("/<route>")
def serve_html(route="index"):
    return render_template(f"{route}.html")


if __name__ == "__main__":
    logger.debug("Development server started")
    app.run(debug=True)
