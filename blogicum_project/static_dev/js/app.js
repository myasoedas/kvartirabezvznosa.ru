(()=>{var t={652:()=>{document.addEventListener("DOMContentLoaded",(function(){var t,e=document.querySelector(".slider__track"),n=document.querySelectorAll(".slider__slide"),o=document.querySelector(".slider__arrow--left"),c=document.querySelector(".slider__arrow--right"),r=document.querySelector(".slider__dots"),d=0,i=n.length;n.forEach((function(t,e){var n=document.createElement("span");n.classList.add("slider__dot"),0===e&&n.classList.add("slider__dot--active"),n.dataset.index=e,r.appendChild(n)}));var s=document.querySelectorAll(".slider__dot");function a(t){e.style.transform="translateX(-".concat(100*t,"%)"),s.forEach((function(t){return t.classList.remove("slider__dot--active")})),s[t].classList.add("slider__dot--active")}function l(){a(d=(d+1)%i)}function u(){clearInterval(t),t=setInterval(l,5e3)}o.addEventListener("click",(function(){a(d=(d-1+i)%i),u()})),c.addEventListener("click",(function(){l(),u()})),s.forEach((function(t){t.addEventListener("click",(function(){a(d=parseInt(t.dataset.index)),u()}))})),t=setInterval(l,5e3)}))}},e={};function n(o){var c=e[o];if(void 0!==c)return c.exports;var r=e[o]={exports:{}};return t[o](r,r.exports,n),r.exports}(()=>{"use strict";var t=n(652);function e(t){"dark"===t?document.body.classList.add("theme-dark"):document.body.classList.remove("theme-dark")}document.addEventListener("DOMContentLoaded",(function(){var n,o,c;n=document.getElementById("hamburger-icon"),o=document.getElementById("popup-menu"),n&&o&&(n.addEventListener("click",(function(t){t.preventDefault(),n.classList.toggle("active"),o.classList.toggle("open"),o.classList.contains("open")?document.body.style.overflow="hidden":document.body.style.overflow=""})),document.addEventListener("click",(function(t){o.contains(t.target)||n.contains(t.target)||(n.classList.remove("active"),o.classList.remove("open"),document.body.style.overflow="")}))),(c=document.getElementById("theme-toggle"))&&(e(localStorage.getItem("theme")||"light"),c.addEventListener("click",(function(){var t="dark"==(document.body.classList.contains("theme-dark")?"dark":"light")?"light":"dark";e(t),localStorage.setItem("theme",t)}))),function(){var t=document.querySelector(".hero__content");if(t){var e=[{title:"Хотите купить квартиру в Москве?",buttons:["Да"]},{title:"У вас есть деньги на первоначальный взнос?",buttons:["Да","Нет"]},{title:"Хотите узнать, какую квартиру вы можете купить?",buttons:["Да"]},{title:"Карина Дерябина - эксперт по недвижимости",buttons:["Получить подборку"],description:"Сделаю для вас подборку лучших вариантов квартир"}],n=0;!function o(){var c=e[n],r=c.title,d=c.buttons,i=c.description;t.innerHTML='\n            <h1 class="hero__title">'.concat(r,"</h1>\n            ").concat(i?'<p class="hero__description">'.concat(i,"</p>"):"",'\n            <div class="hero__buttons">\n                ').concat(d.map((function(t){return'<button class="hero__button">'.concat(t,"</button>")})).join(""),"\n            </div>\n        "),document.querySelectorAll(".hero__button").forEach((function(t){t.addEventListener("click",(function(){n<e.length-1&&(n++,o())}))}))}()}}(),(0,t.slider)()}))})()})();