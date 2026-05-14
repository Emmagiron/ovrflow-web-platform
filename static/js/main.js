/* ======================================
   OVRFLOW MAIN JS
====================================== */

class OVRFLOW {

    constructor() {

        this.lastScroll = 0;

        this.navbar =
            document.querySelector("nav");

        this.menuToggle =
            document.getElementById("menuToggle");

        this.mobileMenu =
            document.getElementById("mobileMenu");

        this.init();

    }

    /* ======================================
       INIT
    ====================================== */

    init() {

        this.initRevealAnimations();
        this.initNavbarEffects();
        this.initMobileMenu();
        this.initSmoothScroll();
        this.initActiveLinks();
        this.initScrollProgress();
        this.initRippleEffect();

    }

    /* ======================================
       REVEAL ANIMATIONS
    ====================================== */

    initRevealAnimations() {

        if (
            typeof initRevealAnimations ===
            "function"
        ) {

            initRevealAnimations();

        }

    }

    /* ======================================
       NAVBAR EFFECTS
    ====================================== */

    initNavbarEffects() {

        if (!this.navbar) return;

        const handleScroll = () => {

            const currentScroll =
                window.scrollY;

            // Scrolled Style
            this.navbar.classList.toggle(
                "nav-scrolled",
                currentScroll > 40
            );

            // Hide / Show Navbar
            if (currentScroll > 120) {

                if (
                    currentScroll >
                    this.lastScroll
                ) {

                    this.navbar.classList.add(
                        "nav-hidden"
                    );

                } else {

                    this.navbar.classList.remove(
                        "nav-hidden"
                    );

                }

            }

            this.lastScroll =
                currentScroll <= 0
                    ? 0
                    : currentScroll;

        };

        window.addEventListener(
            "scroll",
            () => {

                requestAnimationFrame(
                    handleScroll
                );

            },

            { passive: true }

        );

        handleScroll();

    }

    /* ======================================
       MOBILE MENU
    ====================================== */

    initMobileMenu() {

        if (
            !this.menuToggle ||
            !this.mobileMenu
        ) return;

        this.menuToggle.addEventListener(
            "click",
            () => {

                this.mobileMenu.classList.toggle(
                    "active"
                );

                this.menuToggle.classList.toggle(
                    "active"
                );

                document.body.classList.toggle(
                    "menu-open"
                );

            }
        );

        // Close menu on link click
        const mobileLinks =
            this.mobileMenu.querySelectorAll("a");

        mobileLinks.forEach((link) => {

            link.addEventListener(
                "click",
                () => {

                    this.mobileMenu.classList.remove(
                        "active"
                    );

                    this.menuToggle.classList.remove(
                        "active"
                    );

                    document.body.classList.remove(
                        "menu-open"
                    );

                }
            );

        });

        // Close on outside click
        document.addEventListener(
            "click",
            (e) => {

                const clickedOutside =
                    !this.mobileMenu.contains(
                        e.target
                    ) &&
                    !this.menuToggle.contains(
                        e.target
                    );

                if (
                    clickedOutside &&
                    this.mobileMenu.classList.contains(
                        "active"
                    )
                ) {

                    this.mobileMenu.classList.remove(
                        "active"
                    );

                    this.menuToggle.classList.remove(
                        "active"
                    );

                    document.body.classList.remove(
                        "menu-open"
                    );

                }

            }
        );

    }

    /* ======================================
       SMOOTH SCROLL
    ====================================== */

    initSmoothScroll() {

        const links =
            document.querySelectorAll(
                'a[href^="#"]'
            );

        links.forEach((link) => {

            link.addEventListener(
                "click",
                (e) => {

                    const targetId =
                        link.getAttribute("href");

                    if (
                        targetId === "#" ||
                        targetId.length < 2
                    ) return;

                    const target =
                        document.querySelector(
                            targetId
                        );

                    if (!target) return;

                    e.preventDefault();

                    target.scrollIntoView({

                        behavior: "smooth",
                        block: "start"

                    });

                }
            );

        });

    }

    /* ======================================
       ACTIVE NAV LINKS
    ====================================== */

    initActiveLinks() {

        const sections =
            document.querySelectorAll("section[id]");

        const navLinks =
            document.querySelectorAll(
                'nav a[href^="#"]'
            );

        if (
            !sections.length ||
            !navLinks.length
        ) return;

        const observer =
            new IntersectionObserver(

                (entries) => {

                    entries.forEach((entry) => {

                        if (
                            entry.isIntersecting
                        ) {

                            const id =
                                entry.target.id;

                            navLinks.forEach(
                                (link) => {

                                    link.classList.remove(
                                        "active"
                                    );

                                    if (
                                        link.getAttribute(
                                            "href"
                                        ) ===
                                        `#${id}`
                                    ) {

                                        link.classList.add(
                                            "active"
                                        );

                                    }

                                }
                            );

                        }

                    });

                },

                {

                    threshold: 0.55

                }

            );

        sections.forEach((section) => {

            observer.observe(section);

        });

    }

    /* ======================================
       SCROLL PROGRESS BAR
    ====================================== */

    initScrollProgress() {

        const progress =
            document.createElement("div");

        progress.className =
            "scroll-progress";

        document.body.appendChild(
            progress
        );

        const updateProgress = () => {

            const scrollTop =
                window.scrollY;

            const docHeight =
                document.documentElement
                    .scrollHeight -
                window.innerHeight;

            const width =
                (scrollTop / docHeight) * 100;

            progress.style.width =
                `${width}%`;

        };

        window.addEventListener(
            "scroll",
            () => {

                requestAnimationFrame(
                    updateProgress
                );

            },

            { passive: true }

        );

        updateProgress();

    }

    /* ======================================
       RIPPLE EFFECT
    ====================================== */

    initRippleEffect() {

        const buttons =
            document.querySelectorAll(
                ".btn, .btn-whatsapp"
            );

        buttons.forEach((button) => {

            button.addEventListener(
                "click",
                (e) => {

                    const ripple =
                        document.createElement(
                            "span"
                        );

                    ripple.classList.add(
                        "ripple"
                    );

                    const rect =
                        button.getBoundingClientRect();

                    const size =
                        Math.max(
                            rect.width,
                            rect.height
                        );

                    ripple.style.width =
                        ripple.style.height =
                            `${size}px`;

                    ripple.style.left =
                        `${
                            e.clientX -
                            rect.left -
                            size / 2
                        }px`;

                    ripple.style.top =
                        `${
                            e.clientY -
                            rect.top -
                            size / 2
                        }px`;

                    button.appendChild(
                        ripple
                    );

                    setTimeout(() => {

                        ripple.remove();

                    }, 700);

                }
            );

        });

    }

}

/* ======================================
   INIT APP
====================================== */

document.addEventListener(

    "DOMContentLoaded",

    () => {

        new OVRFLOW();

    }

);