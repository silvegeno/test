"use strict";

const form = document.querySelector("#access-form");
const note = document.querySelector("#note");
const count = document.querySelector("#char-count");
const button = document.querySelector("#submit-button");
const status = document.querySelector("#form-status");

function showStatus(message, state) {
  status.replaceChildren();
  status.dataset.state = state;
  status.append(document.createTextNode(message));
}

note.addEventListener("input", () => {
  count.textContent = `${note.value.length} / 500`;
});

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const mock = new URLSearchParams(window.location.search).get("mock");
  button.disabled = true;
  showStatus("Отправляем…", "pending");

  try {
    let response;
    let payload;
    if (["success", "429", "error"].includes(mock)) {
      console.info(`[AI News] mock form response: ${mock}`);
      await new Promise((resolve) => window.setTimeout(resolve, 180));
      const statusCode = mock === "success" ? 200 : Number(mock) || 500;
      response = { ok: statusCode >= 200 && statusCode < 300, status: statusCode };
      payload = mock === "success"
        ? { id: 42, url: "https://t.me/praktik_ai_portfolio_bot?start=r42" }
        : { detail: mock === "429" ? "rate limit" : "network error" };
    } else {
      response = await fetch("https://praktik-ai.ru/api/request", {
        method: "POST",
        headers: { "Content-Type": "application/json", Accept: "application/json" },
        body: JSON.stringify({ project: "rss-ai", note: note.value.trim() }),
      });
      payload = await response.json().catch(() => ({}));
    }

    if (response.status === 429) {
      showStatus("С этого адреса уже отправлено много заявок. Попробуйте позже.", "error");
      return;
    }
    if (!response.ok) {
      showStatus(response.status === 400
        ? "Проект пока не подключён к выдаче ссылок. Попробуйте позже."
        : "Не получилось отправить заявку. Проверьте соединение и повторите попытку.", "error");
      return;
    }

    showStatus(`Заявка №${payload.id} принята. `, "success");
    const link = document.createElement("a");
    link.href = payload.url;
    link.textContent = "Открыть Telegram";
    link.rel = "noopener noreferrer";
    status.append(link);
  } catch {
    showStatus("Не получилось отправить заявку. Проверьте соединение и повторите попытку.", "error");
  } finally {
    button.disabled = false;
  }
});
