/* ======================================
   ADVANCED IMAGE PREVIEW
====================================== */

class ImagePreview {

    constructor() {

        this.maxSize = 5 * 1024 * 1024; // 5MB

        this.allowedFormats = [
            "image/jpeg",
            "image/png",
            "image/webp",
            "image/gif"
        ];

    }

    /* ======================================
       PREVIEW IMAGE
    ====================================== */

    preview(input, previewId, options = {}) {

        const preview =
            document.getElementById(previewId);

        if (!preview || !input) return;

        const config = {

            showInfo: true,
            enableZoom: true,
            rounded: true,
            ...options

        };

        // No file selected
        if (
            !input.files ||
            !input.files[0]
        ) {

            this.resetPreview(
                preview,
                input
            );

            return;

        }

        const file = input.files[0];

        /* ======================================
           VALIDATIONS
        ====================================== */

        // File type
        if (
            !this.allowedFormats.includes(
                file.type
            )
        ) {

            this.showError(
                "Formato no permitido."
            );

            input.value = "";

            return;

        }

        // File size
        if (file.size > this.maxSize) {

            this.showError(
                "La imagen supera 5MB."
            );

            input.value = "";

            return;

        }

        /* ======================================
           LOADING EFFECT
        ====================================== */

        preview.classList.add(
            "preview-loading"
        );

        /* ======================================
           READER
        ====================================== */

        const reader =
            new FileReader();

        reader.onload = (e) => {

            const image =
                new Image();

            image.onload = () => {

                preview.src =
                    e.target.result;

                preview.alt =
                    file.name;

                preview.classList.remove(
                    "hidden",
                    "preview-loading"
                );

                preview.classList.add(
                    "preview-visible"
                );

                // Add style classes
                if (config.rounded) {

                    preview.classList.add(
                        "preview-rounded"
                    );

                }

                // Image info
                if (config.showInfo) {

                    this.createInfo(
                        preview,
                        file,
                        image
                    );

                }

                // Zoom effect
                if (config.enableZoom) {

                    this.enableZoom(
                        preview
                    );

                }

            };

            image.src =
                e.target.result;

        };

        reader.onerror = () => {

            this.showError(
                "Error al cargar imagen."
            );

            preview.classList.remove(
                "preview-loading"
            );

        };

        reader.readAsDataURL(file);

    }

    /* ======================================
       RESET PREVIEW
    ====================================== */

    resetPreview(preview, input = null) {

        preview.src = "";

        preview.alt = "";

        preview.className = "hidden";

        const wrapper =
            preview.parentElement;

        const oldInfo =
            wrapper.querySelector(
                ".preview-info"
            );

        if (oldInfo) {

            oldInfo.remove();

        }

        if (input) {

            input.value = "";

        }

    }

    /* ======================================
       INFO BOX
    ====================================== */

    createInfo(preview, file, image) {

        const wrapper =
            preview.parentElement;

        // Remove previous
        const oldInfo =
            wrapper.querySelector(
                ".preview-info"
            );

        if (oldInfo) {

            oldInfo.remove();

        }

        const info =
            document.createElement("div");

        info.className =
            "preview-info";

        const size =
            (file.size / 1024 / 1024)
                .toFixed(2);

        info.innerHTML = `

            <div class="preview-meta">

                <span>${file.name}</span>

                <small>
                    ${image.width}×${image.height}px
                    • ${size}MB
                </small>

            </div>

        `;

        wrapper.appendChild(info);

    }

    /* ======================================
       ZOOM EFFECT
    ====================================== */

    enableZoom(preview) {

        preview.addEventListener(
            "mousemove",
            (e) => {

                const rect =
                    preview.getBoundingClientRect();

                const x =
                    ((e.clientX - rect.left) /
                        rect.width) *
                    100;

                const y =
                    ((e.clientY - rect.top) /
                        rect.height) *
                    100;

                preview.style.transformOrigin =
                    `${x}% ${y}%`;

            }
        );

        preview.addEventListener(
            "mouseenter",
            () => {

                preview.style.transform =
                    "scale(1.06)";

            }
        );

        preview.addEventListener(
            "mouseleave",
            () => {

                preview.style.transform =
                    "scale(1)";

                preview.style.transformOrigin =
                    "center";

            }
        );

    }

    /* ======================================
       ERROR
    ====================================== */

    showError(message) {

        // Remove old toast
        const oldToast =
            document.querySelector(
                ".preview-toast"
            );

        if (oldToast) {

            oldToast.remove();

        }

        const toast =
            document.createElement("div");

        toast.className =
            "preview-toast";

        toast.innerHTML = `

            <span>${message}</span>

        `;

        document.body.appendChild(
            toast
        );

        requestAnimationFrame(() => {

            toast.classList.add(
                "show"
            );

        });

        setTimeout(() => {

            toast.classList.remove(
                "show"
            );

            setTimeout(() => {

                toast.remove();

            }, 300);

        }, 3000);

    }

}

/* ======================================
   GLOBAL INSTANCE
====================================== */

const imagePreview =
    new ImagePreview();

/* ======================================
   GLOBAL FUNCTION
====================================== */

function previewImage(
    input,
    previewId,
    options = {}
) {

    imagePreview.preview(
        input,
        previewId,
        options
    );

}