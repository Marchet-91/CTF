import express from 'express';
import cookieSession from 'cookie-session';

function isString(value: unknown): value is string {
	return !!value && typeof value === 'string';
}

declare global {
	namespace Express {
		interface Request {
			session: {
				lastTimestamp: number;
				streak: number;
			};
		}
	}
}

const app = express();

app.use(express.urlencoded());
app.use(express.static('./public'));
app.use(
	cookieSession({
		secret: 'REDACTED'
	})
);

app.use((req, res, next) => {
	// initialize streak at 0
	if (!('streak' in req.session) || !req.session.streak) {
		req.session.streak = 0;
	}
	if (!('lastTimestamp' in req.session) || !req.session.lastTimestamp) {
		req.session.lastTimestamp = 0;
	}

	next();
});

app.get('/', (req, res) => {
	res.render('index');
});

app.post('/', (req, res) => {
	let timestamp = req.body.timestamp;
	if (!isString(timestamp)) {
		res.status(400).send('Invalid timestamp');
		return;
	}
	timestamp = Number.parseInt(timestamp, 10);
	if (Number.isNaN(timestamp)) {
		res.status(400).send('Invalid timestamp');
		return;
	}

	if (req.session.lastTimestamp === 0) {
		req.session.streak = 1;
		req.session.lastTimestamp = timestamp;
		res.json({
			streak: req.session.streak,
			message: 'Come back tomorrow to continue your streak!'
		});
		return;
	}

	const last = new Date(req.session.lastTimestamp);
	const lastDay = new Date(last.getUTCFullYear(), last.getUTCMonth(), last.getUTCDate()).getTime();

	// Too soon
	if (timestamp < lastDay + 24 * 60 * 60 * 1000) {
		res.json({
			streak: req.session.streak,
			message: 'Come back tomorrow to continue your streak!'
		});
		return;
	}

	// Skipped a day, reset the streak
	if (timestamp > lastDay + 2 * 24 * 60 * 60 * 1000) {
		req.session.streak = 1;
		req.session.lastTimestamp = timestamp;
		res.json({
			streak: req.session.streak,
			message: 'Come back tomorrow to continue your streak!'
		});
		return;
	}

	// continue streak
	req.session.streak += 1;
	req.session.lastTimestamp = timestamp;
	// if we reach 5, get the flag
	if (req.session.streak === 5) {
		res.json({
			streak: req.session.streak,
			message: process.env.FLAG || 'CCIT{REDACTED}'
		});
	} else {
		res.json({
			streak: req.session.streak,
			message: 'Come back tomorrow to continue your streak!'
		});
	}
});

app.listen(3000, '0.0.0.0', () => {
	console.log('Server is running on http://localhost:3000');
});
