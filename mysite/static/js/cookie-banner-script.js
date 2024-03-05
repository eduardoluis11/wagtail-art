/* Script extra de JavaScript */

/* Snippet del Banner de Consentimiento de Cookies.
*
* Esto está inspirado en el banner de Consentimiento de Cookies de Godson Thomas de aquí:
* https://github.com/eduardoluis11/morosos-en-frances/blob/main/morosidad_app/static/assets/js/main.js .
*  */

// Esto selecciona el div que tiene el botón de "Acepto" de las cookies
const botonDeAceptarCookies = document.querySelector(".boton-aceptar-cookies")

// Div que contiene todo el texto del banner de las cookies
const containerDelBannerDeCookies = document.querySelector(".container-banner-cookies")

// Event listener que instala la cookie en tu navegador si clicas en "Acepto"
botonDeAceptarCookies.addEventListener("click", () => {

    // Esto instala la cookie. Aquí mismo le asignaré el nombre a la cookie
    localStorage.setItem("usuarioHaAceptadoCookies", "true")

    // Esto ocultará permanentemente el banner de las cookies después de hacer clic en "Acepto"
    containerDelBannerDeCookies.classList.remove("active")
})

// Si han pasado 3 segundos, esto le mostrará al usuario el mensaje de las cookies
setTimeout(() => {

    // Si la cookie ya está instalada
    if (!localStorage.getItem("usuarioHaAceptadoCookies")) {
        containerDelBannerDeCookies.classList.add("active")
    }
}, 3000)


/* Fin del snippet del Banner de Consentimiento de Cookies */