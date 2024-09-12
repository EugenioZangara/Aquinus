
// Obtener referencias a los elementos
document.addEventListener("DOMContentLoaded", function() {

    //Anulabos el select de divisiones, si se checkea única division

    const unicaDivisionChk = document.getElementById("unicaDivisionCheck");
    const numeroDivisionesInput = document.getElementById("id_division");

    if (unicaDivisionChk) {
        unicaDivisionChk.addEventListener("change", function () {
            if (unicaDivisionChk.checked) {
                numeroDivisionesInput.value = 1;
                numeroDivisionesInput.disabled = true;
            } else {
                numeroDivisionesInput.disabled = false;
            }
        });
    }


    const crearCursoBtn = document.getElementById("crearCursoBtn");
    const bloqueCargaAlumnos = document.getElementById("bloqueCargaAlumnos");
    
    crearCursoBtn.addEventListener("click", function() {
        // Cambia el estilo `display` a `flex`
        bloqueCargaAlumnos.style.display = "flex";
    
        // Hace scroll hasta el final de la página de manera suave
        window.scrollTo({
            top: document.body.scrollHeight,
            behavior: "smooth"
        });
    });
    

});