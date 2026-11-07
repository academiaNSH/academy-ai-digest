/* Нейродайджест — вся логика страницы.
   Разделы: 1) шапка  2) появление блоков  3) фильтр карточек
            4) прогресс чтения                                      */

(function () {
  "use strict";

  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* 1. Шапка становится плотнее при прокрутке ----------------------------- */
  var header = document.querySelector("[data-header]");

  function updateHeader() {
    if (!header) return;
    header.classList.toggle("is-scrolled", window.scrollY > 12);
  }

  updateHeader();
  window.addEventListener("scroll", updateHeader, { passive: true });

  /* 2. Плавное появление блоков при скролле ------------------------------- */
  var revealItems = document.querySelectorAll(".reveal");

  if (!reduceMotion && "IntersectionObserver" in window) {
    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.15, rootMargin: "0px 0px -40px 0px" }
    );

    revealItems.forEach(function (item) {
      observer.observe(item);
    });
  } else {
    revealItems.forEach(function (item) {
      item.classList.add("is-visible");
    });
  }

  /* 3. Фильтр карточек по теме -------------------------------------------- */
  var filters = document.querySelectorAll("[data-filter]");
  var cards = document.querySelectorAll("[data-category]");
  var countLabel = document.querySelector("[data-count]");

  function plural(number, one, few, many) {
    var mod10 = number % 10;
    var mod100 = number % 100;
    if (mod10 === 1 && mod100 !== 11) return one;
    if (mod10 >= 2 && mod10 <= 4 && (mod100 < 12 || mod100 > 14)) return few;
    return many;
  }

  filters.forEach(function (button) {
    button.addEventListener("click", function () {
      var value = button.dataset.filter;
      var visible = 0;

      filters.forEach(function (item) {
        var isActive = item === button;
        item.classList.toggle("is-active", isActive);
        item.setAttribute("aria-pressed", String(isActive));
      });

      cards.forEach(function (card) {
        var show = value === "all" || card.dataset.category === value;
        card.classList.toggle("is-hidden", !show);
        if (show) visible += 1;
      });

      if (countLabel) {
        countLabel.textContent =
          visible + " " + plural(visible, "материал", "материала", "материалов");
      }
    });
  });

  /* 4. Полоса прогресса чтения на странице материала ---------------------- */
  var progress = document.querySelector("[data-progress]");

  function updateProgress() {
    if (!progress) return;
    var root = document.documentElement;
    var scrollable = root.scrollHeight - root.clientHeight;
    var percent = scrollable > 0 ? (root.scrollTop / scrollable) * 100 : 0;
    progress.style.width = percent + "%";
  }

  if (progress) {
    updateProgress();
    window.addEventListener("scroll", updateProgress, { passive: true });
    window.addEventListener("resize", updateProgress);
  }
})();
