let home = `{{ home }}`;
let about = `{{ about }}`;
let blog = `{{ blog }}`;
let invalidPage = "<h1>404 - Page Not Found!</h1>";

const routes = {
    "/": home,
    "/about": about,
    "/blog": blog,
    default: invalidPage,
};

const render = path => {
    console.log('path: ' + path);
    const content = routes[path] || invalidPage;

    document.querySelector("#root").innerHTML = content;
};

// Add a single click event listener for all links that navigate within the site
document.addEventListener("click", evt => {
    const target = evt.target;
    if (target.tagName === "A" && target.getAttribute("href").startsWith("/")) {
        evt.preventDefault();
        const { pathname: path } = new URL(target.href);
        render(path);
        window.history.pushState({ path }, path, path);
    }
});

window.addEventListener("popstate", e => {
    render(new URL(window.location.href).pathname);
});

window.onload = function init() {
    render("/");
};
