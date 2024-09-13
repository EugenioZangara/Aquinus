
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
    


    
});

