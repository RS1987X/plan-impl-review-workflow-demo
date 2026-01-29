import express from 'express';

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware to parse JSON requests
app.use(express.json());

// Sample route to demonstrate the workflow
app.get('/', (req, res) => {
    res.send('AI Workflow Worktrees Test Application');
});

// Start the server
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});