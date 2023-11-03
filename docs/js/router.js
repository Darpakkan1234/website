let home = `<h1>Welcome!</h1>
<ul>
<li>Head over to <code>/about</code> to know more about me.</li>
<li>Head over to <code>/blog</code> to read my posts.</li>
</ul>
<p>Well, Hope you do not waste much of your time here on this useless website.</p>`;
let about = `<h1>Hello! This is someone.</h1>
<p>Some sample text.</p>`;
let blog = `<h1 class="text-2xl font-bold mb-4">BLOG</h1>

<ul class="list-disc pl-6">
    
    <li class="mb-2">
        <a href="First_Post" class="text-blue-500 hover:underline">First Post</a> (2023-10-30)
    </li>
    
</ul>`;
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