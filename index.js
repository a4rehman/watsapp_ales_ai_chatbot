require('dotenv').config();
const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode');
const express = require('express');
const http = require('http');
const socketIo = require('socket.io');
const { GoogleGenerativeAI } = require("@google/generative-ai");

const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);
const aiModel = genAI.getGenerativeModel({ model: "gemini-1.5-flash" });

const app = express();
const server = http.createServer(app);
const io = socketIo(server);
const session = require('express-session');
const path = require('path');
const port = process.env.PORT || 5000;
const ACCESS_CODE = process.env.ACCESS_CODE || "123456"; // Default code if not in .env

app.use(express.urlencoded({ extended: true }));
app.use(session({
    secret: 'secret-key-abdul-rehman',
    resave: false,
    saveUninitialized: true
}));

// Initialize WhatsApp Client
const client = new Client({
    authStrategy: new LocalAuth(),
    webVersionCache: {
        type: 'remote',
        remotePath: 'https://raw.githubusercontent.com/wppconnect-team/wa-version/main/html/2.2412.54.html',
    },
    puppeteer: {
        headless: true,
        args: [
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-dev-shm-usage',
            '--disable-accelerated-2d-canvas',
            '--no-first-run',
            '--no-zygote',
            '--disable-gpu',
            '--hide-scrollbars',
            '--disable-notifications',
            '--disable-background-timer-throttling',
            '--disable-backgrounding-occluded-windows',
            '--disable-breakpad',
            '--disable-component-extensions-with-background-pages',
            '--disable-extensions',
            '--disable-features=TranslateUI,BlinkGenPropertyTrees',
            '--disable-ipc-flooding-protection',
            '--disable-renderer-backgrounding',
            '--enable-features=NetworkService,NetworkServiceInProcess'
        ],
    }
});

// Explicit error catching for initialization
client.on('auth_failure', msg => {
    console.error('AUTHENTICATION FAILURE', msg);
});

client.on('disconnected', (reason) => {
    console.log('Client was logged out', reason);
});

// Web UI Routes
app.get('/', (req, res) => {
    if (req.session.authorized) {
        res.send(`
            <html>
                <head>
                    <title>AI Bot Dashboard</title>
                    <meta name="viewport" content="width=device-width, initial-scale=1">
                    <style>
                        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
                        body { font-family: 'Inter', sans-serif; text-align: center; margin: 0; padding: 20px; background: #0b141a; color: white; display: flex; align-items: center; justify-content: center; min-height: 100vh; }
                        .container { background: #1c2b33; padding: 40px; border-radius: 20px; display: inline-block; box-shadow: 0 15px 35px rgba(0,0,0,0.5); border: 1px solid #2a3942; max-width: 450px; width: 100%; transition: all 0.3s ease; }
                        #qrcode { margin: 30px auto; width: 250px; height: 250px; background: white; border-radius: 12px; display: flex; align-items: center; justify-content: center; padding: 10px; overflow: hidden; box-shadow: 0 0 20px rgba(37, 211, 102, 0.2); }
                        #qrcode img { width: 100%; height: auto; }
                        .status { font-size: 1.1em; font-weight: 600; padding: 10px 20px; border-radius: 50px; background: rgba(37, 211, 102, 0.1); color: #25d366; display: inline-block; margin-top: 15px; }
                        h1 { color: #f0f2f5; margin-bottom: 10px; font-weight: 700; letter-spacing: -1px; }
                        p { color: #8696a0; line-height: 1.5; margin-bottom: 20px; }
                        .logout { margin-top: 30px; display: block; color: #ef4444; text-decoration: none; font-size: 0.9em; transition: opacity 0.3s; }
                        .logout:hover { opacity: 0.8; }
                        .badge { background: #25d366; color: #0b141a; font-size: 0.7em; padding: 3px 8px; border-radius: 4px; vertical-align: middle; margin-left: 5px; }
                    </style>
                </head>
                <body>
                    <div class="container">
                        <h1>CAR SHOWROOM AI <span class="badge">PRO</span></h1>
                        <p>Cloud AI Workflow is Ready. Scan the QR code to connect your WhatsApp.</p>
                        <div id="qrcode">
                            <div style="color: #666">Loading AI System...</div>
                        </div>
                        <div id="status" class="status">Waiting for System...</div>
                        <a href="/logout" class="logout">Secure Logout</a>
                    </div>
                    <script src="/socket.io/socket.io.js"></script>
                    <script>
                        const socket = io();
                        socket.on('qr', (url) => {
                            document.getElementById('qrcode').innerHTML = '<img src="' + url + '" />';
                            document.getElementById('status').innerHTML = 'Scan QR Code Now';
                        });
                        socket.on('ready', () => {
                            document.getElementById('qrcode').innerHTML = '<h1 style="color: #25d366; font-size: 4em;">✓</h1>';
                            document.getElementById('status').innerHTML = 'ACTIVE: AI is Replying';
                            document.getElementById('status').style.background = 'rgba(37, 211, 102, 0.2)';
                        });
                        socket.on('message', (msg) => {
                            // Subtle activity log
                            console.log('Bot Activity:', msg);
                        });
                    </script>
                </body>
            </html>
        `);
    } else {
        res.send(`
            <html>
                <head>
                    <title>AI Dashboard Login</title>
                    <meta name="viewport" content="width=device-width, initial-scale=1">
                    <style>
                        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
                        body { font-family: 'Inter', sans-serif; height: 100vh; margin: 0; background: #0b141a; display: flex; align-items: center; justify-content: center; }
                        .login-box { background: #1c2b33; padding: 50px; border-radius: 20px; border: 1px solid #2a3942; box-shadow: 0 20px 50px rgba(0,0,0,0.5); text-align: center; width: 380px; }
                        h2 { color: #f0f2f5; margin-bottom: 30px; font-weight: 700; letter-spacing: -0.5px; }
                        input { width: 100%; padding: 15px; margin-bottom: 25px; border: 1px solid #2a3942; background: #0b141a; color: white; border-radius: 10px; box-sizing: border-box; font-size: 16px; outline: none; transition: border-color 0.3s; }
                        input:focus { border-color: #25d366; }
                        button { width: 100%; padding: 15px; background: #25d366; color: #0b141a; border: none; border-radius: 10px; cursor: pointer; font-size: 16px; font-weight: 700; transition: transform 0.2s, background 0.3s; }
                        button:hover { background: #1ed760; transform: translateY(-2px); }
                        button:active { transform: translateY(0); }
                        .error { color: #ef4444; margin-bottom: 20px; font-size: 0.9em; font-weight: 600; }
                        .footer { color: #8696a0; font-size: 0.8em; margin-top: 30px; }
                    </style>
                </head>
                <body>
                    <div class="login-box">
                        <h2>🔒 PRIVATE AI ACCESS</h2>
                        <form action="/login" method="POST">
                            <input type="password" name="code" placeholder="Enter Access Code" required autofocus>
                            ${req.query.error ? '<p class="error">Incorrect access code.</p>' : ''}
                            <button type="submit">Unlock Dashboard</button>
                        </form>
                        <div class="footer">Built by AI Engineer Abdul Rehman</div>
                    </div>
                </body>
            </html>
        `);
    }
});

app.post('/login', (req, res) => {
    if (req.body.code === ACCESS_CODE) {
        req.session.authorized = true;
        res.redirect('/');
    } else {
        res.redirect('/?error=1');
    }
});

app.get('/logout', (req, res) => {
    req.session.destroy();
    res.redirect('/');
});

// WhatsApp Events
client.on('qr', (qr) => {
    qrcode.toDataURL(qr, (err, url) => {
        io.emit('qr', url);
        console.log('QR Code generated, scan in browser!');
    });
});

client.on('ready', () => {
    io.emit('ready');
    console.log('WhatsApp Bot is Ready!');
});

const startTime = Math.floor(Date.now() / 1000);

client.on('message', async (msg) => {
    // 1. Ignore if it's a group message
    if (msg.from.includes('@g.us')) return;

    // 2. Ignore messages that were received before the bot started
    if (msg.timestamp < startTime) return;

    console.log('Incoming Message:', msg.body);
    io.emit('message', 'Processing: ' + msg.body);

    try {
        const prompt = `System: You are an expert Car Sales & Service Assistant for a premium Car Showroom. Your goal is to guide customers on car buying and service. Reply in English or Hindi (Roman OK). Keep it concise. Built by Abdul Rehman.
        
        User: ${msg.body}`;

        const result = await aiModel.generateContent(prompt);
        const response = await result.response;
        const reply = response.text();

        msg.reply(reply);
        console.log('AI Reply:', reply);
    } catch (error) {
        console.error('AI Error:', error);
    }
});

client.initialize();

server.listen(port, () => {
    console.log(`Web interface running on http://localhost:${port}`);
});
