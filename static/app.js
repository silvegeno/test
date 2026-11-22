const newsList = document.querySelector("#news-list");
const refreshButton = document.querySelector("#refresh");
const resultCount = document.querySelector("#result-count");
const updatedAt = document.querySelector("#updated-at");

function appendText(parent, tag, className, text) {
  const element = document.createElement(tag);
  if (className) element.className = className;
  element.textContent = text || "";
  parent.append(element);
  return element;
}

function formatDate(value) {
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return "Дата не указана";
  return new Intl.DateTimeFormat("ru-RU", {
    dateStyle: "medium",
    timeStyle: "short",
  }).format(date);
}

function renderNews(items) {
  newsList.replaceChildren();
  if (!items.length) {
    const empty = appendText(newsList, "p", "message", "В этой ленте пока нет новостей.");
    empty.setAttribute("role", "status");
    resultCount.textContent = "НЕТ ПУБЛИКАЦИЙ";
    return;
  }

  items.forEach((item, index) => {
    const card = document.createElement("article");
    card.className = "news-card";
    appendText(card, "span", "card-number", String(index + 1).padStart(2, "0"));

    const content = document.createElement("div");
    appendText(content, "p", "card-date", formatDate(item.published));
    appendText(content, "h2", "card-title", item.title || "Без заголовка");
    appendText(content, "p", "card-description", item.description || "Описание отсутствует.");
    card.append(content);

    try {
      const url = new URL(item.link);
      if (url.protocol === "https:" || url.protocol === "http:") {
        const link = appendText(card, "a", "card-link", "↗");
        link.href = url.href;
        link.target = "_blank";
        link.rel = "noopener noreferrer";
        link.setAttribute("aria-label", "Открыть оригинал статьи");
      }
    } catch {
      // Ignore malformed feed URLs rather than rendering unsafe links.
    }

    newsList.append(card);
  });
  resultCount.textContent = `${items.length} ${items.length === 1 ? "ПУБЛИКАЦИЯ" : "ПУБЛИКАЦИЙ"}`;
}

async function loadNews() {
  refreshButton.disabled = true;
  newsList.setAttribute("aria-busy", "true");
  resultCount.textContent = "ОБНОВЛЯЕМ ЛЕНТУ";
  const icon = refreshButton.querySelector(".refresh-icon");
  icon.textContent = "…";

  try {
    const response = await fetch("/api/news?limit=5", { headers: { Accept: "application/json" } });
    if (!response.ok) {
      const payload = await response.json().catch(() => ({}));
      throw new Error(payload.detail || `Ошибка загрузки: ${response.status}`);
    }
    const data = await response.json();
    renderNews(data.items || []);
    updatedAt.textContent = data.updated_at
      ? `ОБНОВЛЕНО ${new Date(data.updated_at).toLocaleTimeString("ru-RU", { hour: "2-digit", minute: "2-digit" })}`
      : "";
  } catch (error) {
    newsList.replaceChildren();
    const message = appendText(newsList, "p", "message error", error.message || "Не удалось загрузить новости.");
    message.setAttribute("role", "alert");
    resultCount.textContent = "ОШИБКА ЗАГРУЗКИ";
    updatedAt.textContent = "";
  } finally {
    refreshButton.disabled = false;
    newsList.setAttribute("aria-busy", "false");
    icon.textContent = "↻";
  }
}

refreshButton.addEventListener("click", loadNews);
loadNews();
