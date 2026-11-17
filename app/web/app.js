// Frontend: HTML/CSS/JS polos (tanpa npm/bundler). Panggil Python lewat `api()`.
const $ = (id) => document.getElementById(id);
const api = () => window.pywebview.api;

function toast(msg, ms = 2200) {
  const el = $("toast");
  el.textContent = msg;
  el.classList.add("show");
  clearTimeout(toast._t);
  toast._t = setTimeout(() => el.classList.remove("show"), ms);
}

function applyTheme(theme) {
  document.documentElement.dataset.theme = theme;
}

async function init() {
  const info = await api().app_info();
  document.title = info.name;
  $("app-name").textContent = info.name;
  $("app-version").textContent = "v" + info.version;
  $("info").innerHTML = [
    ["Mode", info.frozen ? "exe (build)" : "dev"],
    ["Python", info.python],
    ["Folder Data", info.data_dir],
  ].map(([k, v]) => `<dt>${k}</dt><dd>${v}</dd>`).join("");

  const settings = await api().get_settings();
  applyTheme(settings.theme || "dark");

  $("btn-ping").onclick = async () => toast(await api().ping());
  $("btn-data").onclick = () => api().open_data_folder();
  $("btn-theme").onclick = async () => {
    const next = document.documentElement.dataset.theme === "dark" ? "light" : "dark";
    applyTheme(next);
    await api().set_setting("theme", next);
  };
}

// pywebview baru siap setelah event ini
window.addEventListener("pywebviewready", init);
