const tiles = [...document.querySelectorAll('.table-tile')];
const selectedInput = document.getElementById('selected-table');
const message = document.getElementById('form-message');
const modal = document.getElementById('auth-modal');
const closeModal = document.getElementById('close-modal');
const checkBtn = document.getElementById('check-btn');
const form = document.getElementById('booking-form');

function setMessage(text) {
    message.textContent = text;
}

function selectedValues() {
    return {
        date: document.getElementById('date').value,
        time: document.getElementById('time').value,
        guests: Number(document.getElementById('guests').value),
        zone: document.getElementById('zone').value,
    };
}

function clearSelection() {
    selectedInput.value = '';
    tiles.forEach((tile) => tile.classList.remove('selected'));
}

tiles.forEach((tile) => {
    tile.addEventListener('click', () => {
        if (tile.classList.contains('busy') || tile.classList.contains('hidden')) {
            return;
        }
        clearSelection();
        tile.classList.add('selected');
        selectedInput.value = tile.dataset.tableId;
        setMessage(`Обрано столик ${tile.querySelector('span').textContent}.`);
    });
});

async function checkAvailability() {
    const values = selectedValues();
    if (!values.date || !values.time || !values.guests) {
        setMessage('Вкажи дату, час і кількість гостей.');
        return;
    }

    const query = `
        query AvailableTables($date: Date!, $time: Time!, $guests: Int!, $zone: String) {
            availableTables(date: $date, time: $time, guests: $guests, zone: $zone) {
                id
            }
        }
    `;

    const response = await fetch('/graphql/', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            query,
            variables: {
                date: values.date,
                time: values.time,
                guests: values.guests,
                zone: values.zone || null,
            },
        }),
    });
    const data = await response.json();
    const availableIds = new Set((data.data?.availableTables || []).map((table) => String(table.id)));

    clearSelection();
    tiles.forEach((tile) => {
        const seatOk = Number(tile.dataset.seats) >= values.guests;
        const zoneOk = !values.zone || tile.dataset.zone === values.zone;
        tile.classList.toggle('hidden', !seatOk || !zoneOk);
        tile.classList.toggle('busy', !availableIds.has(tile.dataset.tableId) && seatOk && zoneOk);
        tile.classList.toggle('free', availableIds.has(tile.dataset.tableId));
    });

    setMessage(`Знайдено доступних столиків: ${availableIds.size}.`);
}

checkBtn.addEventListener('click', checkAvailability);

form.addEventListener('submit', async (event) => {
    event.preventDefault();

    if (!window.bookingConfig.isAuthenticated) {
        modal.hidden = false;
        return;
    }

    const values = selectedValues();
    if (!selectedInput.value) {
        setMessage('Спочатку обери доступний столик.');
        return;
    }

    const response = await fetch('/api/reservations/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': window.bookingConfig.csrfToken,
        },
        body: JSON.stringify({
            table: selectedInput.value,
            date: values.date,
            time: values.time,
            guests: values.guests,
            customer_name: document.getElementById('customer_name').value,
            phone: document.getElementById('phone').value,
        }),
    });

    if (response.ok) {
        setMessage('Бронювання створено.');
        await checkAvailability();
    } else {
        const error = await response.json();
        setMessage(JSON.stringify(error));
    }
});

closeModal.addEventListener('click', () => {
    modal.hidden = true;
});

const protocol = window.location.protocol === 'https:' ? 'wss' : 'ws';
const socket = new WebSocket(`${protocol}://${window.location.host}/ws/tables/`);

socket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    const values = selectedValues();
    const sameSlot = data.date === values.date && data.time === values.time;
    const tile = document.querySelector(`[data-table-id="${data.table_id}"]`);
    if (tile && sameSlot) {
        tile.classList.remove('free', 'selected');
        tile.classList.add('busy');
        if (selectedInput.value === String(data.table_id)) {
            selectedInput.value = '';
        }
        setMessage('Статус столика оновлено наживо через WebSocket.');
    }
};

const today = new Date().toISOString().slice(0, 10);
document.getElementById('date').value = today;
checkAvailability();
