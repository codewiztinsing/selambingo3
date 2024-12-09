const express = require('express');
const app = express();
const http = require('http').createServer(app);
const io = require('socket.io')(http);

// Game state
let games = {};

// Generate random bingo card
function generateBingoCard() {
    let card = [];
    let used = new Set();
    
    // Generate numbers for each column B(1-15), I(16-30), N(31-45), G(46-60), O(61-75)
    for (let col = 0; col < 5; col++) {
        let column = [];
        let min = col * 15 + 1;
        let max = min + 14;
        
        while (column.length < 5) {
            let num = Math.floor(Math.random() * (max - min + 1)) + min;
            if (!used.has(num)) {
                used.add(num);
                column.push(num);
            }
        }
        card.push(column);
    }
    
    // Make center space free
    card[2][2] = "FREE";
    
    return card;
}

io.on('connection', (socket) => {
    console.log('A user connected');
    
    // Create new game
    socket.on('create_game', (data) => {
        const gameId = Math.random().toString(36).substring(7);
        games[gameId] = {
            players: [{
                id: socket.id,
                card: generateBingoCard(),
                name: data.playerName
            }],
            numbers_called: [],
            current_turn: 0,
            status: 'waiting'
        };
        
        socket.join(gameId);
        socket.emit('game_created', { gameId: gameId, card: games[gameId].players[0].card });
    });
    
    // Join existing game
    socket.on('join_game', (data) => {
        const gameId = data.gameId;
        if (games[gameId] && games[gameId].status === 'waiting') {
            games[gameId].players.push({
                id: socket.id,
                card: generateBingoCard(),
                name: data.playerName
            });
            
            socket.join(gameId);
            socket.emit('game_joined', { 
                card: games[gameId].players[games[gameId].players.length - 1].card 
            });
            
            if (games[gameId].players.length >= 2) {
                games[gameId].status = 'playing';
                io.to(gameId).emit('game_started');
            }
        }
    });
    
    // Call number
    socket.on('call_number', (data) => {
        const gameId = data.gameId;
        if (games[gameId] && games[gameId].status === 'playing') {
            let number;
            do {
                number = Math.floor(Math.random() * 75) + 1;
            } while (games[gameId].numbers_called.includes(number));
            
            games[gameId].numbers_called.push(number);
            io.to(gameId).emit('number_called', { number: number });
        }
    });
    
    // Bingo claim
    socket.on('bingo', (data) => {
        const gameId = data.gameId;
        if (games[gameId]) {
            const player = games[gameId].players.find(p => p.id === socket.id);
            if (player) {
                // Verify win logic here
                games[gameId].status = 'finished';
                io.to(gameId).emit('game_won', { 
                    winner: player.name 
                });
            }
        }
    });
    
    socket.on('disconnect', () => {
        console.log('User disconnected');
        // Clean up games where this socket was a player
        for (let gameId in games) {
            games[gameId].players = games[gameId].players.filter(p => p.id !== socket.id);
            if (games[gameId].players.length === 0) {
                delete games[gameId];
            }
        }
    });
});
// Serve static files and index.html
app.use(express.static('empirebingo'));
app.get('/', (req, res) => {
    // Generate a unique game ID if needed
    let gameId = Object.keys(games)[0];
    if (!gameId) {
        gameId = Math.random().toString(36).substring(7);
        games[gameId] = {
            players: [],
            status: 'waiting',
            numbers_called: []
        };
    }
    
    // Add game ID to session/query params when serving index.html
    res.redirect(`/?gameId=${gameId}`);
});



const PORT = process.env.PORT || 3000;
http.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});

