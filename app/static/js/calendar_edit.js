document.addEventListener('DOMContentLoaded', function() {
    // Configuration
    const MODES = ['mode-eco', 'mode-confort', 'mode-off'];
    const gridData = Array(7).fill().map(() => Array(96).fill('mode-eco')); // État initial
    
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
                alert('Planning sauvegardé avec succès !');
            } else {
                alert('Erreur lors de la sauvegarde du planning');
            }
        })
        .catch(error => {
            console.error('Erreur:', error);
            alert('Erreur lors de la sauvegarde du planning');
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
