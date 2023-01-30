class key {

	constructor(w, h, content, code, appearance) {
		this.w = w;
		this.h = h;
		this.content = content;
		this.code = code;
		this.appearance = appearance;

		this.isDown = false;
		this.prevDown = false;
	}

	draw(x, y) {
		strokeWeight(this.appearance["strokeWeight"]);
		stroke(this.appearance["stroke"]);
		fill(this.appearance["fill"]);
		rect(x, y, this.w, this.h, this.appearance["borderRad"]);
		noFill();
		textSize(this.h / 2);
		textFont(this.appearance["font"]);
		textAlign(CENTER, CENTER);
		text(this.content, x + this.w / 2, y + this.h / 2 + 1);
	}

	update(w, h) {
		this.w = w;
		this.h = h;
		this.appearance.borderRad = keySize / 7;
		this.appearance.strokeWeight = keySize / 25;
		this.prevDown = this.isDown;
		this.isDown = keyIsDown(this.code);
	}

}

class Keyboard {

	constructor(keySize, style) {
		this.style = style;
		this.defaultKeyApp = {
			stroke: this.style["upStroke"],
			fill: this.style["upFill"],
			strokeWeight: this.style["strokeWeight"],
			font: this.style["font"],
			borderRad: this.style["borderRad"]
		};

		this.keycodes = [81, 87, 69, 82, 84, 89, 85, 73, 79, 80, 65, 83, 68, 70, 71, 72, 74, 75, 76, 90, 88, 67, 86, 66, 78, 77];
		this.spaceKeycode = 32;
		this.altKeycode = 18;

		this.keySize = keySize;
		this.altWidth = keySize * 1.3;
		this.spaceWidth = keySize * 6.7;

		this.pressed = new Array(26);
		this.immune = new Array(26);

		this.kbOffset = - 2 * this.spaceWidth;
		this.yOffsets = new Array(26);
		this.animationSpeed = 15;

		this.numbers = new Array(26);

		this.keys = new Array(26);
		for (let i = 0; i < 26; i++) {
			this.keys[i] = new key(keySize, keySize, "", this.keycodes[i], Object.assign({}, this.defaultKeyApp));
		}
		this.space = new key(this.spaceWidth, this.keySize, "start", this.spaceKeycode, Object.assign({}, this.defaultKeyApp));
		this.alt = new key(this.altWidth, this.keySize, "", this.altKeycode, Object.assign({}, this.defaultKeyApp));

		this.initialize();
	}

	static shuffle(array) {
		let currentIndex = array.length, randomIndex;

		while (currentIndex != 0) {
			randomIndex = Math.floor(Math.random() * currentIndex);
			currentIndex--;

			[array[currentIndex], array[randomIndex]] = [array[randomIndex], array[currentIndex]];
		}

		return array;
	}

	width() {
		return (this.keySize + this.keySize / 7) * 9 + this.keySize;
	}

	height() {
		return (this.keySize + this.keySize / 7) * 3 + this.keySize;
	}

	start() {
		let numbers = new Array(26);
		for (let i = 0; i < 26; i++) {
			numbers[i] = i + 1;
		}
		Keyboard.shuffle(numbers);

		this.state = 2;
		this.numbers = numbers;
		for (let i = 0; i < 26; i++) {
			this.keys[i].content = numbers[i];
		}
		this.space.content = this.time;
	}

	startCountdown() {
		this.state = 1;

		this.keys[13].content = "";
		this.keys[14].content = "";
		this.keys[15].content = "";
		this.keys[16].content = "";
	}

	initialize() {
		this.state = 0;
		this.time = 0;
		this.cdTime = 180;
		this.scoreDelay = 60;
		this.mistakes = 0;
		this.expectedNext = 1;

		for (let i = 0; i < 26; i++) {
			this.keys[i].content = "";
		}
		this.keys[13].content = "1";
		this.keys[14].content = "-";
		this.keys[15].content = "2";
		this.keys[16].content = "6";
		this.space.content = "start";
		this.alt.content = "";

		for (let i = 0; i < this.keys.length; i++) {
			this.keys[i].appearance = Object.assign({}, this.defaultKeyApp);
			this.pressed[i] = false;
			this.immune[i] = false;
		}
		this.space.appearance = Object.assign({}, this.defaultKeyApp);
		this.alt.appearance = Object.assign({}, this.defaultKeyApp);
		this.alt.appearance["fill"] = this.style["upMistakeFill"];
		this.alt.appearance["stroke"] = this.style["upMistakeStroke"];

		for (let i = 0; i < this.yOffsets.length; i++) {
			this.yOffsets[i] = this.kbOffset + i * (this.keySize / 3);
		}
		this.spaceOffset = - 2 * this.spaceWidth;
		this.altOffset = this.spaceOffset / 2;
	}

	draw(x, y) {
		let rowOffsets = [0, 2 * this.keySize / 7, this.keySize, this.keySize * 1.3];

		/* draws row 1 of letter keys */
		for (let i = 0; i < 10; i++) {
			this.keys[i].draw(x + rowOffsets[0] + i * (this.keySize + this.keySize / 7) - this.width() / 2,
				y + this.yOffsets[i] - this.height() / 2);
		}
		/* draws row 2 of letter keys */
		for (let i = 0; i < 9; i++) {
			this.keys[i + 10].draw(x + rowOffsets[1] + i * (this.keySize + this.keySize / 7) - this.width() / 2,
				y + this.yOffsets[i + 10] + this.keySize + this.keySize / 7 - this.height() / 2);
		}
		/* draws row 3 of letter keys */
		for (let i = 0; i < 7; i++) {
			this.keys[i + 19].draw(x + rowOffsets[2] + i * (this.keySize + this.keySize / 7) - this.width() / 2,
				y + this.yOffsets[i + 19] + 2 * (this.keySize + this.keySize / 7) - this.height() / 2);
		}

		this.space.draw(x + this.spaceOffset + rowOffsets[3] + this.altWidth + this.keySize / 7 - this.width() / 2,
			y + 3 * (this.keySize + this.keySize / 7) - this.height() / 2);
		this.alt.draw(x + this.altOffset + rowOffsets[3] - this.width() / 2,
			y + 3 * (this.keySize + this.keySize / 7) - this.height() / 2);
	}

	update(keySize) {
		this.keySize = keySize;
		this.altWidth = keySize * 1.3;
		this.spaceWidth = keySize * 6.7;
		for (let i = 0; i < this.keys.length; i++) {
			this.keys[i].update(this.keySize, this.keySize);
		}
		this.space.update(this.spaceWidth, this.keySize);
		this.alt.update(this.altWidth, this.keySize);

		switch (this.state) {
			case 0:

				if (this.spaceOffset < - this.animationSpeed) {
					this.spaceOffset += this.animationSpeed;
				} else {
					this.spaceOffset = 0;
				}
				for (let i = 0; i < this.yOffsets.length; i++) {
					if (this.yOffsets[i] < - this.animationSpeed) {
						this.yOffsets[i] += this.animationSpeed;
					} else {
						this.yOffsets[i] = 0;
					}
				}

				this.space.update(this.spaceWidth, this.keySize);

				if (this.space.isDown && ingame) {
					this.startCountdown();
				}

				break;
			case 1:

				if (this.spaceOffset < - this.animationSpeed) {
					this.spaceOffset += this.animationSpeed;
				} else {
					this.spaceOffset = 0;
				}
				for (let i = 0; i < this.yOffsets.length; i++) {
					if (this.yOffsets[i] < - this.animationSpeed) {
						this.yOffsets[i] += this.animationSpeed;
					} else {
						this.yOffsets[i] = 0;
					}
				}

				if (this.cdTime == 180) {
					this.space.content = "3";
				} else if (this.cdTime == 120) {
					this.space.content = "2";
				} else if (this.cdTime == 60) {
					this.space.content = "1";
				} else if (this.cdTime == 0) {
					this.start();
				}

				this.cdTime--;

				break;
			case 2:

				this.space.content = (Math.round(this.time / 60 * 100) / 100).toFixed(2);
				this.alt.content = this.mistakes;

				if (this.mistakes > 0) {
					if (this.altOffset < - this.animationSpeed) {
						this.altOffset += this.animationSpeed;
					} else {
						this.altOffset = 0;
					}
				}

				this.time++;
				for (let i = 0; i < 26; i++) {
					if (this.keys[i].isDown && ingame) {
						if (this.keys[i].content == this.expectedNext) {
							this.pressed[i] = true;
							this.immune[i] = true;
							this.keys[i].appearance["stroke"] = this.style["downStroke"];
							this.keys[i].appearance["fill"] = this.style["downFill"];
							this.expectedNext++;
						} else if (!this.immune[i]) {
							this.keys[i].appearance["stroke"] = this.pressed[i] ? this.style["downMistakeStroke"] : this.style["upMistakeStroke"];
							this.keys[i].appearance["fill"] = this.pressed[i] ? this.style["downMistakeFill"] : this.style["upMistakeFill"];
							if (!this.keys[i].prevDown) {
								this.mistakes++;
							}
						}
					} else if (this.keys[i].prevDown) {
						this.immune[i] = false;
						this.keys[i].appearance["stroke"] = this.pressed[i] ? this.style["downStroke"] : this.style["upStroke"];
						this.keys[i].appearance["fill"] = this.pressed[i] ? this.style["downFill"] : this.style["upFill"];
					}
					this.keys[i].update(this.keySize, this.keySize);
				}
				this.space.update(this.spaceWidth, this.keySize);
				this.alt.update(this.altWidth, this.keySize);

				if (this.expectedNext == 27) {
					for (let i = 0; i < 26; i++) {
						this.keys[i].appearance["stroke"] = this.style["downStroke"];
						this.keys[i].appearance["fill"] = this.style["downFill"];
					}

					this.state = 3;
				}

				break;
			case 3:

				if (this.scoreDelay > 0) {
					this.scoreDelay--;
				}

				for (let i = 0; i < this.yOffsets.length; i++) {
					this.yOffsets[i] -= this.animationSpeed * 1.5;
				}
				if (this.scoreDelay == 0) {
					this.spaceOffset += this.animationSpeed * 1.5;
					if (this.mistakes > 0) {
						this.altOffset += this.animationSpeed * 1.5;
					}
				}

				if (this.spaceOffset > this.spaceWidth * 2) {
					this.initialize();
				}

				break;
		}
	}

}




let defaultStyle = {
	upStroke: "#c8c8c8",
	upFill: "#604060",
	upMistakeStroke: "#e8c8c8",
	upMistakeFill: "#a04060",
	downStroke: "#686868",
	downFill: "#301630",
	downMistakeStroke: "#a06868",
	downMistakeFill: "#601630",
	highlightStroke: "#e8e8e8",
	highlightFill: "#806080",

	strokeWeight: 2,
	font: "Courier New",
	borderRad: 7
};




let ingame = true;

window.addEventListener("click", (e) => {
	console.log(e.target);
	if (e.target === document.getElementsByTagName("canvas")[0]) {
		ingame = true;
	} else {
		ingame = false;
	}
});

window.addEventListener('keydown', e => {
	if (e.key === ' ' && ingame) {
		e.preventDefault();
	}
});



let canvasWidth = 720;
let canvasHeight = (1 / 2) * canvasWidth;
let cnv;
let sketch = document.getElementById('sketch');

let keySize = 50;

let k = new Keyboard(keySize, defaultStyle);

function setup() {

	frameRate(60);
	cnv = createCanvas(canvasWidth, canvasHeight);
	cnv.parent("sketch");

}

function draw() {

	sketchWidth = sketch.offsetWidth;
	canvasWidth = sketchWidth;
	canvasHeight = (1 / 2) * canvasWidth;
	resizeCanvas(canvasWidth, canvasHeight);

	background("#160714");

	keySize = (1 / 15) * width;
	k.update(keySize);
	k.draw(canvasWidth / 2, canvasHeight / 2);

}
