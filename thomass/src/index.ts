import express from 'express';
import { DatabaseSync } from 'node:sqlite';
import db from './database';
import cookieSession from 'cookie-session';

function isString(value: unknown): value is string {
	return !!value && typeof value === 'string';
}

declare global {
	namespace Express {
		interface Request {
			db: DatabaseSync;
			session: { cart: Record<number, { name: string; image: string; price: number; amount: number }> };
		}
	}
}

const app = express();

app.use(express.urlencoded());
app.set('view engine', 'ejs');
app.use(express.static('./public'));
app.use(
	cookieSession({
		secret: 'REDACTED'
	})
);

app.use((req, res, next) => {
	req.db = db;

	db.exec(`CREATE TABLE IF NOT EXISTS products (
		id INTEGER PRIMARY KEY,
		name VARCHAR(255) NOT NULL,
		description TEXT NOT NULL,
		price DECIMAL(10, 2) NOT NULL,
		image VARCHAR(255) NOT NULL
	);`);

	db.exec(`CREATE TABLE IF NOT EXISTS coupons (
		code VARCHAR(255) NOT NULL PRIMARY KEY,
		amount DECIMAL(10, 2) NOT NULL
	);`);

	db.exec(
		`INSERT INTO products 
		(id, name, description, price, image) 
		VALUES 
		(1, 'metal pipe', 'The original metal pipe percussion instrument, drop it to have its iconic sound played.', 1337.00, '/metal-pipe.png'),
		(2, 'metal pipe flute', 'The sweet and mellow sound of a flute.', 499.97, '/metal-pipe-flute.png'),
		(3, 'metal pipe organ', 'Great for every genre', 12345.67, '/metal-pipe-organ.png'), -- original picture: by J.Hannan-Briggs https://www.geograph.org.uk/reuse.php?id=2926323#credit
		(4, 'metal pipe drumsticks', 'Give power to your percussion performances!', 30.45, '/metal-pipe-drumsticks.png'),
		(5, 'tubular bells', 'The original metal pipe, but with more notes!', 10000.00, '/tubular-bells.png') -- original picture: by Xylosmygame https://en.wikipedia.org/wiki/File:Yamaha_Deagan_chimes_(from_LA_Percussion_Rentals).jpg
		ON CONFLICT (id) DO NOTHING;`
	);

	db.exec(
		`INSERT INTO coupons
		(code, amount)
		VALUES
		('REDACTED', 999999999)
		ON CONFLICT (code) DO NOTHING;`
	);

	if (!('cart' in req.session) || !req.session.cart) {
		req.session.cart = {};
	}

	next();
});

app.get('/', (req, res) => {
	const query = req.db.prepare('SELECT * FROM products LIMIT 3');
	const products = query.all();
	res.render('index', { products: products });
});

app.get('/list', (req, res) => {
	let sort: string = (req.query.sort as string | undefined) ?? 'id';
	let sortOrder = 'ASC';	
	if (sort[0] == '-') {
		sort = sort.substring(1);
		sortOrder = 'DESC';
	}
	const limit = req.query.limit ?? 5;	
	const query = req.db.prepare(`SELECT * FROM products ORDER BY ${sort} ${sortOrder} LIMIT ${limit}`);
	const products = query.all();
	res.render('list', { products: products });
});

app.get('/product/:id', (req, res) => {
	const query = req.db.prepare('SELECT * FROM products WHERE id = ?');
	const product = query.get(req.params.id);
	if (!product) {
		res.status(404).send('404 not found');
		return;
	}
	res.render('product', { product: product });
});

app.post('/product/:id', (req, res) => {
	const query = req.db.prepare('SELECT * FROM products WHERE id = ?');
	const product = query.get(req.params.id);
	if (!product) {
		res.status(404).send('404 not found');
		return;
	}
	if ((product.id as number) in req.session.cart) {
		req.session.cart[product.id as number].amount++;
	} else {
		req.session.cart[product.id as number] = {
			name: product.name as string,
			image: product.image as string,
			amount: 1,
			price: product.price as number
		};
	}

	res.redirect('/cart');
});

app.get('/cart', (req, res) => {
	res.render('cart', { cart: req.session.cart });
});

app.post('/checkout', (req, res) => {
	const count = Object.values(req.session.cart).reduce(
		(prev, prod) => (prod.amount > 0 ? prev + prod.amount : prev),
		0
	);
	const price = Object.values(req.session.cart).reduce(
		(prev, prod) => (prod.amount > 0 ? prev + prod.amount * prod.price : prev),
		0
	);

	const couponCode = req.body.coupon;
	if (!isString(couponCode)) {
		res.status(400).send('Invalid coupon code');
		return;
	}

	const query = req.db.prepare('SELECT * FROM coupons WHERE code = ?');
	const coupon = query.get(couponCode);
	if (!coupon) {
		res.status(404).send('Coupon not found');
		return;
	}

	if (count > 0 && price > 0 && price < Number(coupon.amount)) {
		res.send(process.env.FLAG || 'CCIT{REDACTED}');
	} else {
		res.status(412).send('Not enough money');
	}
});

app.listen(3000, '0.0.0.0', () => {
	console.log('Server is running on http://localhost:3000');
});
