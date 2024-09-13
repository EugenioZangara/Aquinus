
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


    const btnCargarAlumnos = document.getElementById("btnCargarAlumnos");
    const areaCargaAlumnos = document.getElementById("bloqueCargaAlumnos");

    if (btnCargarAlumnos) {
        btnCargarAlumnos.addEventListener("click", cargarAlumnos);
       
    } else {
        console.error("No se encontró el botón con id btnCargarAlumnos");
    }

    function cargarAlumnos() {
        numeroDivisionesInput.disabled = true;
        areaCargaAlumnos.style.display = "flex";
        const appBody = document.getElementById('app-body');
        if (appBody) {
            appBody.scrollTo({
                top: appBody.scrollHeight,
                behavior: 'smooth'
            });
        } else {
            console.warn('No se encontró el elemento con id app-body');
        }
    }
    


    
});

