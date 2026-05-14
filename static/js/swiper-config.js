/* ======================================
   OVRFLOW HERO SWIPER
====================================== */

document.addEventListener(

    "DOMContentLoaded",

    () => {

        const swiperContainer =
            document.querySelector(".mySwiper");

        if (!swiperContainer) return;

        const swiper =
            new Swiper(".mySwiper", {

                /* ======================================
                   CORE
                ====================================== */

                loop: true,

                speed: 1100,

                grabCursor: true,

                centeredSlides: true,

                watchSlidesProgress: true,

                preloadImages: false,

                lazy: {

                    loadPrevNext: true,

                },

                /* ======================================
                   EFFECT
                ====================================== */

                effect: "creative",

                creativeEffect: {

                    prev: {

                        shadow: true,

                        translate: ["-18%", 0, -1],

                        scale: 0.92,

                        opacity: 0.65,

                    },

                    next: {

                        translate: ["18%", 0, -1],

                        scale: 0.92,

                        opacity: 0.65,

                    },

                },

                /* ======================================
                   AUTOPLAY
                ====================================== */

                autoplay: {

                    delay: 5000,

                    disableOnInteraction: false,

                    pauseOnMouseEnter: true,

                },

                /* ======================================
                   PAGINATION
                ====================================== */

                pagination: {

                    el: ".swiper-pagination",

                    clickable: true,

                    dynamicBullets: true,

                    renderBullet: function (
                        index,
                        className
                    ) {

                        return `

                            <span class="${className}">

                                <span class="bullet-inner"></span>

                            </span>

                        `;

                    },

                },

                /* ======================================
                   NAVIGATION
                ====================================== */

                navigation: {

                    nextEl:
                        ".swiper-button-next",

                    prevEl:
                        ".swiper-button-prev",

                },

                /* ======================================
                   KEYBOARD + MOUSE
                ====================================== */

                keyboard: {

                    enabled: true,

                    onlyInViewport: true,

                },

                mousewheel: {

                    forceToAxis: true,

                },

                /* ======================================
                   PARALLAX
                ====================================== */

                parallax: true,

                /* ======================================
                   BREAKPOINTS
                ====================================== */

                breakpoints: {

                    0: {

                        slidesPerView: 1,

                        spaceBetween: 18,

                    },

                    768: {

                        slidesPerView: 1.1,

                        spaceBetween: 24,

                    },

                    1200: {

                        slidesPerView: 1.2,

                        spaceBetween: 32,

                    },

                },

                /* ======================================
                   EVENTS
                ====================================== */

                on: {

                    init() {

                        animateActiveSlide();

                    },

                    slideChangeTransitionStart() {

                        animateActiveSlide();

                    },

                },

            });

        /* ======================================
           ACTIVE SLIDE ANIMATION
        ====================================== */

        function animateActiveSlide() {

            const slides =
                document.querySelectorAll(
                    ".swiper-slide"
                );

            slides.forEach((slide) => {

                slide.classList.remove(
                    "slide-active"
                );

            });

            const activeSlide =
                document.querySelector(
                    ".swiper-slide-active"
                );

            if (activeSlide) {

                activeSlide.classList.add(
                    "slide-active"
                );

            }

        }

        /* ======================================
           VISIBILITY API
        ====================================== */

        document.addEventListener(
            "visibilitychange",
            () => {

                if (document.hidden) {

                    swiper.autoplay.stop();

                } else {

                    swiper.autoplay.start();

                }

            }
        );

    }

);