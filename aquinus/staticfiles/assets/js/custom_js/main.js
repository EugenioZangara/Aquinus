



const toastLiveExample = document.getElementById('liveToast');

// Función para mostrar el toast
function mostrarToast() {
  
            $('.toast').toast({
                animation: false,
                delay: 3000
            });
            $('.toast').toast('show');
        
}