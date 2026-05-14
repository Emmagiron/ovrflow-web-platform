/* ======================================
   OVRFLOW WHATSAPP ORDERS
====================================== */

class WhatsAppOrders {

    constructor() {

        this.phone = "5493624866422";

        this.storeName = "OVRFLOW";

    }

    /* ======================================
       SEND ORDER
    ====================================== */

    sendOrder(
        codigo,
        nombre,
        id,
        precioUnitario,
        precioOferta = 0,
        cantidadOferta = 0
    ) {

        const cantidadInput =
            document.getElementById(
                `cant-${id}`
            );

        const talleSelect =
            document.getElementById(
                `talle-${id}`
            );

        /* ======================================
           VALIDATIONS
        ====================================== */

        if (!cantidadInput) {

            this.showToast(
                "No se encontró la cantidad."
            );

            return;

        }

        const cantidad =
            parseInt(cantidadInput.value) || 1;

        if (cantidad <= 0) {

            this.showToast(
                "Cantidad inválida."
            );

            cantidadInput.focus();

            return;

        }

        const talle =
            talleSelect?.value ||
            "Único";

        /* ======================================
           CALCULATE TOTAL
        ====================================== */

        const pricing =
            this.calculateTotal(

                cantidad,
                precioUnitario,
                precioOferta,
                cantidadOferta

            );

        const total =
            pricing.total;

        const ahorro =
            pricing.ahorro;

        const tieneOferta =
            pricing.tieneOferta;

        /* ======================================
           FORMAT
        ====================================== */

        const totalFormateado =
            this.formatPrice(total);

        const precioFormateado =
            this.formatPrice(
                precioUnitario
            );

        /* ======================================
           DATE
        ====================================== */

        const fecha =
            new Date()
                .toLocaleString(
                    "es-AR",
                    {

                        day: "2-digit",

                        month: "2-digit",

                        year: "numeric",

                        hour: "2-digit",

                        minute: "2-digit"

                    }
                );

        /* ======================================
           MESSAGE
        ====================================== */

        let mensaje = `

🛍️ *NUEVO PEDIDO - ${this.storeName}*

━━━━━━━━━━━━━━

📦 *Producto:* ${nombre}

🏷️ *Código:* ${codigo}

📏 *Talle:* ${talle}

🔢 *Cantidad:* ${cantidad}

💲 *Precio Unitario:* $${precioFormateado}

━━━━━━━━━━━━━━

💰 *TOTAL:* $${totalFormateado}

`;

        // Offer
        if (tieneOferta) {

            mensaje += `

🔥 *PROMO APLICADA*

🎁 Oferta:
${cantidadOferta} unidades por
$${this.formatPrice(precioOferta)}

💸 Ahorrás:
$${this.formatPrice(ahorro)}

`;

        }

        mensaje += `

━━━━━━━━━━━━━━

📅 ${fecha}

✅ Hola! Quiero confirmar disponibilidad.

`;

        /* ======================================
           ENCODE
        ====================================== */

        const mensajeCodificado =
            encodeURIComponent(
                mensaje
            );

        /* ======================================
           OPEN WHATSAPP
        ====================================== */

        const whatsappURL =

            `https://wa.me/${this.phone}?text=${mensajeCodificado}`;

        window.open(

            whatsappURL,

            "_blank",

            "noopener,noreferrer"

        );

        /* ======================================
           SUCCESS FX
        ====================================== */

        this.showToast(
            "Redirigiendo a WhatsApp..."
        );

        this.buttonFeedback(id);

    }

    /* ======================================
       CALCULATE TOTAL
    ====================================== */

    calculateTotal(
        cantidad,
        precioUnitario,
        precioOferta,
        cantidadOferta
    ) {

        let total = 0;

        let ahorro = 0;

        let tieneOferta = false;

        // Offer logic
        if (

            precioOferta > 0 &&
            cantidadOferta > 0 &&
            cantidad >= cantidadOferta

        ) {

            tieneOferta = true;

            const combos =
                Math.floor(
                    cantidad /
                    cantidadOferta
                );

            const sobrantes =
                cantidad %
                cantidadOferta;

            total =

                (combos * precioOferta) +

                (sobrantes *
                    precioUnitario);

            // Savings
            const precioNormal =

                cantidad *
                precioUnitario;

            ahorro =
                precioNormal - total;

        } else {

            total =
                precioUnitario *
                cantidad;

        }

        return {

            total,
            ahorro,
            tieneOferta

        };

    }

    /* ======================================
       FORMAT PRICE
    ====================================== */

    formatPrice(value) {

        return Number(value)
            .toLocaleString(

                "es-AR",

                {

                    minimumFractionDigits: 0

                }

            );

    }

    /* ======================================
       BUTTON FEEDBACK
    ====================================== */

    buttonFeedback(id) {

        const button =
            document.querySelector(
                `[data-product-id="${id}"]`
            );

        if (!button) return;

        const original =
            button.innerHTML;

        button.classList.add(
            "sending"
        );

        button.innerHTML = `

            ✓ Abriendo WhatsApp

        `;

        setTimeout(() => {

            button.innerHTML =
                original;

            button.classList.remove(
                "sending"
            );

        }, 2200);

    }

    /* ======================================
       TOAST
    ====================================== */

    showToast(message) {

        const oldToast =
            document.querySelector(
                ".wa-toast"
            );

        if (oldToast) {

            oldToast.remove();

        }

        const toast =
            document.createElement(
                "div"
            );

        toast.className =
            "wa-toast";

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

            }, 350);

        }, 2600);

    }

}

/* ======================================
   GLOBAL INSTANCE
====================================== */

const waOrders =
    new WhatsAppOrders();

/* ======================================
   GLOBAL FUNCTION
====================================== */

function enviarPedido(
    codigo,
    nombre,
    id,
    precioUnitario,
    precioOferta,
    cantidadOferta
) {

    waOrders.sendOrder(

        codigo,
        nombre,
        id,
        precioUnitario,
        precioOferta,
        cantidadOferta

    );

}