// ======================================
// ADVANCED REVEAL ANIMATIONS
// ======================================

function initRevealAnimations() {

    const revealElements = document.querySelectorAll(".reveal");

    if (!revealElements.length) return;

    // ======================================
    // CONFIG
    // ======================================

    const CONFIG = {

        threshold: 0.12,

        rootMargin: "0px 0px -80px 0px",

        staggerDelay: 90,

        once: true

    };

    // ======================================
    // SET INITIAL DELAYS
    // ======================================

    revealElements.forEach((element, index) => {

        // Custom stagger animation
        element.style.setProperty(
            "--reveal-delay",
            `${index * CONFIG.staggerDelay}ms`
        );

        // GPU acceleration
        element.style.willChange =
            "opacity, transform";

    });

    // ======================================
    // INTERSECTION OBSERVER
    // ======================================

    const observer = new IntersectionObserver(

        (entries) => {

            entries.forEach((entry) => {

                const element = entry.target;

                if (entry.isIntersecting) {

                    requestAnimationFrame(() => {

                        element.classList.add("active");

                    });

                    // Animate children with stagger
                    const staggerItems =
                        element.querySelectorAll(
                            ".reveal-item"
                        );

                    staggerItems.forEach((item, i) => {

                        item.style.transitionDelay =
                            `${i * 120}ms`;

                        item.classList.add("active");

                    });

                    // Animate only once
                    if (CONFIG.once) {

                        observer.unobserve(element);

                    }

                } else {

                    // Optional: remove animation
                    if (!CONFIG.once) {

                        element.classList.remove("active");

                    }

                }

            });

        },

        {

            threshold: CONFIG.threshold,

            rootMargin: CONFIG.rootMargin

        }

    );

    // ======================================
    // OBSERVE ELEMENTS
    // ======================================

    revealElements.forEach((element) => {

        observer.observe(element);

    });

    // ======================================
    // PARALLAX SUPPORT
    // ======================================

    const parallaxElements =
        document.querySelectorAll("[data-parallax]");

    if (parallaxElements.length) {

        let ticking = false;

        const updateParallax = () => {

            const scrollY = window.scrollY;

            parallaxElements.forEach((element) => {

                const speed =
                    parseFloat(
                        element.dataset.parallax
                    ) || 0.15;

                const offset = scrollY * speed;

                element.style.transform =
                    `translate3d(0, ${offset}px, 0)`;

            });

            ticking = false;

        };

        window.addEventListener(
            "scroll",
            () => {

                if (!ticking) {

                    requestAnimationFrame(updateParallax);

                    ticking = true;

                }

            },

            { passive: true }

        );

    }

    // ======================================
    // MAGNETIC HOVER EFFECT
    // ======================================

    const magneticElements =
        document.querySelectorAll("[data-magnetic]");

    magneticElements.forEach((element) => {

        const strength =
            parseFloat(
                element.dataset.magnetic
            ) || 20;

        element.addEventListener("mousemove", (e) => {

            const rect =
                element.getBoundingClientRect();

            const x =
                e.clientX - rect.left - rect.width / 2;

            const y =
                e.clientY - rect.top - rect.height / 2;

            element.style.transform =
                `translate(${x / strength}px, ${y / strength}px)`;

        });

        element.addEventListener("mouseleave", () => {

            element.style.transform =
                "translate(0px, 0px)";

        });

    });

}

// ======================================
// AUTO INIT
// ======================================

document.addEventListener(

    "DOMContentLoaded",

    () => {

        initRevealAnimations();

    }

);