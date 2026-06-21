document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".claim-form").forEach((form) => {
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      const itemId = form.dataset.id;
      const nameInput = form.querySelector("input[name='name']");
      const feedback = document.getElementById(`feedback-${itemId}`);
      const btn = form.querySelector("button");
      const name = nameInput.value.trim();

      if (!name) {
        feedback.textContent = "Please enter your name.";
        feedback.className = "form-feedback err";
        return;
      }

      btn.disabled = true;
      btn.textContent = "Claiming…";
      feedback.textContent = "";
      feedback.className = "form-feedback";

      const formData = new FormData();
      formData.append("name", name);

      try {
        const res = await fetch(`/claim/${itemId}`, {
          method: "POST",
          body: formData,
        });
        const data = await res.json();

        if (res.ok && data.success) {
          form.innerHTML = "";
          feedback.textContent = `✓ Claimed! The owner will be in touch, ${name}.`;
          feedback.className = "form-feedback ok";

          const card = form.closest(".item-card");
          if (card) {
            card.classList.add("is-claimed");
            const photoWrap = card.querySelector(".card-photo-wrap");
            if (photoWrap && !photoWrap.querySelector(".claimed-badge")) {
              const badge = document.createElement("div");
              badge.className = "claimed-badge";
              badge.textContent = "Claimed";
              photoWrap.appendChild(badge);
            }
          }
        } else {
          feedback.textContent = data.error || "Something went wrong. Try again.";
          feedback.className = "form-feedback err";
          btn.disabled = false;
          btn.textContent = "I want this";
        }
      } catch {
        feedback.textContent = "Network error. Please try again.";
        feedback.className = "form-feedback err";
        btn.disabled = false;
        btn.textContent = "I want this";
      }
    });
  });
});
