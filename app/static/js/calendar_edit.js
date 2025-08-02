document.addEventListener('DOMContentLoaded', function() {
    // Configuration
    const MODES = ['mode-eco', 'mode-confort', 'mode-off'];
    
    // Conversion du planning initial en données de grille
    function convertModeFromBackend(mode) {
        switch(mode) {
            case 'ECO': return 'mode-eco';
            case 'CONFORT': return 'mode-confort';
            case 'OFF': return 'mode-off';
            default: return 'mode-eco';
        }
    }

    // Initialisation de la grille avec les données existantes
    const gridData = [
        initialSchedule.monday,
        initialSchedule.tuesday,
        initialSchedule.wednesday,
        initialSchedule.thursday,
        initialSchedule.friday,
        initialSchedule.saturday,
        initialSchedule.sunday
    ].map(day => day.map(convertModeFromBackend));
    
    // Sélection des éléments du DOM
    const calendar = document.querySelector('.calendar-grid');
    const validateButton = document.getElementById('validate-button');

    // Fonction pour obtenir le mode suivant
    function getNextMode(currentMode) {
        const currentIndex = MODES.indexOf(currentMode);
        return MODES[(currentIndex + 1) % MODES.length];
    }

    // Fonction pour mettre à jour une cellule
    function updateCell(cell, newMode) {
        // Retire tous les modes existants
        MODES.forEach(mode => cell.classList.remove(mode));
        // Ajoute le nouveau mode
        cell.classList.add(newMode);
        // Met à jour les données
        const day = parseInt(cell.dataset.day);
        const slot = parseInt(cell.dataset.slot);
        gridData[day][slot] = newMode;
    }

    // Gestion du clic sur une cellule
    document.querySelectorAll('.time-cell').forEach(cell => {
        // Initialise la cellule avec le mode sauvegardé
        const day = parseInt(cell.dataset.day);
        const slot = parseInt(cell.dataset.slot);
        updateCell(cell, gridData[day][slot]);

        // Gestion du clic
        cell.addEventListener('click', function() {
            // Trouve le mode actuel
            const currentMode = MODES.find(mode => this.classList.contains(mode));
            // Passe au mode suivant
            const nextMode = getNextMode(currentMode);
            updateCell(this, nextMode);
        });
    });

    // Fonction pour convertir les modes en format attendu par le backend
    function convertModeForBackend(mode) {
        switch(mode) {
            case 'mode-eco': return 'ECO';
            case 'mode-confort': return 'CONFORT';
            case 'mode-off': return 'OFF';
            default: return 'ECO';
        }
    }

    // Gestion de la sélection multiple par glisser-déposer
    let isSelecting = false;
    let startCell = null;
    let modeToApply = null;

    calendar.addEventListener('mousedown', function(e) {
        const cell = e.target.closest('.time-cell');
        if (!cell) return;

        isSelecting = true;
        startCell = cell;
        // Le mode à appliquer sera le mode suivant du mode actuel
        modeToApply = getNextMode(MODES.find(mode => cell.classList.contains(mode)));
        updateCell(cell, modeToApply);
    });

    document.addEventListener('mousemove', function(e) {
        if (!isSelecting) return;
        
        const cell = e.target.closest('.time-cell');
        if (!cell) return;

        updateCell(cell, modeToApply);
    });

    document.addEventListener('mouseup', function() {
        isSelecting = false;
        startCell = null;
    });

    // Envoi des données au serveur lors de la validation
    validateButton.addEventListener('click', function() {
        const schedule = {
            schedule: {
                monday: gridData[0].map(convertModeForBackend),
                tuesday: gridData[1].map(convertModeForBackend),
                wednesday: gridData[2].map(convertModeForBackend),
                thursday: gridData[3].map(convertModeForBackend),
                friday: gridData[4].map(convertModeForBackend),
                saturday: gridData[5].map(convertModeForBackend),
                sunday: gridData[6].map(convertModeForBackend)
            }
        };

        // Envoi des données au backend
        fetch('/calendar/set', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(schedule)
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Crée un toast de succès
                const toastContainer = document.querySelector('.toast-container');
                const successToast = document.createElement('div');
                successToast.className = 'toast align-items-center text-white bg-success border-0';
                successToast.setAttribute('role', 'alert');
                successToast.setAttribute('aria-atomic', 'true');
                successToast.innerHTML = `
                    <div class="d-flex">
                        <div class="toast-body">
                            Planning sauvegardé avec succès
                        </div>
                        <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
                    </div>
                `;
                toastContainer.appendChild(successToast);
                
                const toast = new bootstrap.Toast(successToast, {
                    autohide: true,
                    delay: 1000
                });
                
                // Supprime le toast du DOM après qu'il soit caché
                successToast.addEventListener('hidden.bs.toast', function () {
                    successToast.remove();
                });
                
                toast.show();
                
                // Attend que le toast soit affiché avant de rediriger
                setTimeout(() => {
                    window.location.href = '/';
                }, 1000);
            } else {
                // En cas d'erreur, on crée un toast d'erreur dynamiquement
                const toastContainer = document.querySelector('.toast-container');
                const errorToast = document.createElement('div');
                errorToast.className = 'toast align-items-center text-white bg-danger border-0';
                errorToast.setAttribute('role', 'alert');
                errorToast.setAttribute('aria-atomic', 'true');
                errorToast.innerHTML = `
                    <div class="d-flex">
                        <div class="toast-body">
                            Erreur : ${data.error || 'Erreur lors de la sauvegarde'}
                        </div>
                        <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
                    </div>
                `;
                toastContainer.appendChild(errorToast);
                const toast = new bootstrap.Toast(errorToast, {
                    autohide: true,
                    delay: 3000
                });
                toast.show();
                // Supprime le toast du DOM après qu'il soit caché
                errorToast.addEventListener('hidden.bs.toast', function () {
                    errorToast.remove();
                });
            }
        })
        .catch(error => {
            console.error('Erreur:', error);
            // Même chose pour les erreurs de réseau
            const toastContainer = document.querySelector('.toast-container');
            const errorToast = document.createElement('div');
            errorToast.className = 'toast align-items-center text-white bg-danger border-0';
            errorToast.setAttribute('role', 'alert');
            errorToast.setAttribute('aria-atomic', 'true');
            errorToast.innerHTML = `
                <div class="d-flex">
                    <div class="toast-body">
                        Erreur réseau lors de la sauvegarde
                    </div>
                    <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
                </div>
            `;
            toastContainer.appendChild(errorToast);
            const toast = new bootstrap.Toast(errorToast, {
                autohide: true,
                delay: 3000
            });
            toast.show();
            // Supprime le toast du DOM après qu'il soit caché
            errorToast.addEventListener('hidden.bs.toast', function () {
                errorToast.remove();
            });
        });
    });

    // Raccourcis clavier
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            isSelecting = false;
            startCell = null;
        }
    });
});
