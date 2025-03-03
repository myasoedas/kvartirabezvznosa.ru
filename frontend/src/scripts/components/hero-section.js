export function initHeroSection() {
    const heroContent = document.querySelector(".hero__content");
    if (!heroContent) return; // ✅ Проверка, чтобы не было ошибки, если секция отсутствует

    const steps = [
        { title: "Хотите купить квартиру в Москве?", buttons: ["Да"] },
        { title: "У вас есть деньги на первоначальный взнос?", buttons: ["Да", "Нет"] },
        { title: "Хотите узнать, какую квартиру вы можете купить?", buttons: ["Да"] },
        { title: "Карина Дерябина - эксперт по недвижимости", buttons: ["Получить подборку"], description: "Сделаю для вас подборку лучших вариантов квартир" }
    ];
    
    let currentStep = 0;

    function updateStep() {
        const { title, buttons, description } = steps[currentStep];

        heroContent.innerHTML = `
            <h1 class="hero__title">${title}</h1>
            ${description ? `<p class="hero__description">${description}</p>` : ""}
            <div class="hero__buttons">
                ${buttons.map((text) => `<button class="hero__button">${text}</button>`).join("")}
            </div>
        `;

        document.querySelectorAll(".hero__button").forEach(button => {
            button.addEventListener("click", () => {
                if (currentStep < steps.length - 1) {
                    currentStep++;
                    updateStep();
                }
            });
        });
    }

    updateStep();
}
