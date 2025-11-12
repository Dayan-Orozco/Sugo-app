////////////////////// USERS

function ActivateUser(id) {
    Swal.fire({
        title: "¿Confirmar Activacion de Usuaria?",
        text: "Se marcará como Activada y podra acceder al sistema.",
        icon: "question",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "Sí, activar",
        cancelButtonText: "Cancelar"
    }).then((result) => {
        if (result.isConfirmed) {
            window.location.href = `/user/streamers/${id}/activate/`;
        }
    });
}

////////////////////// STREAMERS 

function confirmCapacitar(id) {
    Swal.fire({
        title: "¿Confirmar capacitación?",
        text: "Se marcará como capacitada y se registrará la fecha actual.",
        icon: "question",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "Sí, confirmar",
        cancelButtonText: "Cancelar"
    }).then((result) => {
        if (result.isConfirmed) {
            window.location.href = `/streamers/${id}/capacitar/`;
        }
    });
}

function deleteStreamer(id) { //ELIMINAR STREAMER - CAMBIA ESTADO A LIBERADA
    Swal.fire({
        title: "¿Eliminar Streamer?",
        text: "Esta acción no se puede deshacer.",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "Sí, eliminar",
        cancelButtonText: "Cancelar",
    }).then((result) => {
        if (result.isConfirmed) {
            window.location.href = `/streamers/${id}/delete/`;
        }
    });
}

function setJoinDate(id) { 
    Swal.fire({
        title: 'Asignar Fecha de Registro',
        html: `<input id="joinDateInput" 
                     type="text" 
                     class="form-control" 
                     placeholder="Ej: 2025-04-23 04:25:40">`,
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: 'Guardar',
        cancelButtonText: 'Cancelar',
        preConfirm: () => {
            const dateValue = document.getElementById('joinDateInput').value.trim();
            const formato = /^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$/;

            if (!dateValue) {
                Swal.showValidationMessage('Por favor ingresa una fecha y hora');
                return false;
            }
            if (!formato.test(dateValue)) {
                Swal.showValidationMessage('Formato inválido. Usa YYYY-MM-DD HH:MM:SS');
                return false;
            }
            return dateValue;
        }
    }).then((result) => {
        if (result.isConfirmed) {
            document.getElementById('joinDateHidden').value = result.value;
            document.getElementById('setJoinDateForm').submit();
        }
    });
}
