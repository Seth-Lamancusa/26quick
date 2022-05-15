class key {
	
	constructor (w, h, content, code, appearance) {
		this.w = w;
		this.h = h;
		this.content = content;
		this.code = code;
		this.appearance = appearance;
		
		this.isDown;
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
		text(this.content, x + this.w / 2, y + this.h / 2);
	}
	
	update() {
		this.prevDown = this.isDown;
		this.isDown = keyIsDown(this.code);
	}
	
	setContent(content) {
		this.content = content;
	}
	
}





class Keyboard {
	
	constructor(keySize, style) {
		
		this.style = style;
		this.state = 0;
		this.time = 0;
		this.mistakes = 0;
		this.keySize = keySize;
		
		this.keycodes = [81, 87, 69, 82, 84, 89, 85, 73, 79, 80, 65, 83, 68, 70, 71, 72, 74, 75, 76, 90, 88, 67, 86, 66, 78, 77, 32, 18];
		this.defaultKeyApp = {
			stroke : this.style["upStroke"],
			fill : this.style["upFill"],
			strokeWeight : this.style["strokeWeight"],
			font : this.style["font"],
			borderRad : this.style["borderRad"]
		};
		
		this.altWidth = keySize * 1.3;
		this.spaceWidth = keySize * 7;
		
		this.pressed = new Array(26);
		this.immune = new Array(26);
		this.pressed.fill(false);
		this.immune.fill(false);
		
		this.numbers = new Array(26);
		this.expectedNext = 1;
		
		this.keys = new Array(28);
		for (let i = 0; i < 26; i++) {
			this.keys[i] = new key(keySize, keySize, "", this.keycodes[i], Object.assign({}, this.defaultKeyApp));
		}
		this.keys[13].setContent("1");
		this.keys[14].setContent("-");
		this.keys[15].setContent("2");
		this.keys[16].setContent("6");
		this.keys[26] = new key(this.spaceWidth, this.keySize, "start", this.keycodes[26], this.defaultKeyApp);
		this.keys[27] = new key(this.altWidth, this.keySize, "", this.keycodes[27], this.defaultKeyApp);
		
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
	
	start() {
		let numbers = new Array(26);
		for (let i = 0; i < 26; i++) {
			numbers[i] = i + 1;
		}
		Keyboard.shuffle(numbers);
		
		this.state = 1;
		this.numbers = numbers;
		for (let i = 0; i < 26; i++) {
			this.keys[i].setContent(numbers[i]);
		}
	}
	
	draw(x, y, style) {
		
		console.log(this.keys.isDown);
		
		let rowOffsets = [0, 2 * this.keySize / 7, this.keySize, this.keySize * 1.6];
		
		/* draws row 1 of letter keys */
		for (let i = 0; i < 10; i++) {
			this.keys[i].draw(x + rowOffsets[0] + i * (this.keySize + this.keySize / 7), y);
		}
		/* draws row 2 of letter keys */
		for (let i = 0; i < 9; i++) {
			this.keys[i + 10].draw(x + rowOffsets[1] + i * (this.keySize + this.keySize / 7), y + this.keySize + this.keySize / 7);
		}
		/* draws row 3 of letter keys */
		for (let i = 0; i < 7; i++) {
			this.keys[i + 19].draw(x + rowOffsets[2] + i * (this.keySize + this.keySize / 7), y + 2 * (this.keySize + this.keySize / 7));
		}
		
		/* draws space bar */
		this.keys[26].draw(x + rowOffsets[3] + this.altWidth + this.keySize / 7, y + 3 * (this.keySize + this.keySize / 7));
		
		/* draws left alt */
		this.keys[27].draw(x + rowOffsets[3], y + 3 * (this.keySize + this.keySize / 7));
	
	}
	
	update() {
		
		switch (this.state) {
			case 0:
			
				for (let i = 0; i < 28; i++) {
					this.keys[i].update();
				}
			
				if (this.keys[26].isDown) {
					this.start();
				}
				
				break;
			case 1:
				
				this.keys[26].setContent((Math.round(this.time / 60 * 100) / 100).toFixed(2));
				this.keys[27].setContent(this.mistakes);
				
				this.time++;
				for (let i = 0; i < 26; i++) {
					this.keys[i].update();
					if (this.keys[i].isDown) {
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
				}
				
				break;
			case 2:
				
				break;
		}
		
		if (this.expectedNext == 27) {
			this.state = 2;
		}
		
	}
	
}




let defaultStyle = {
	upStroke : "#c8c8c8",
	upFill : "#604060",
	upMistakeStroke : "#e8c8c8",
	upMistakeFill : "#a04060",
	downStroke : "#686868",
	downFill : "#301630",
	downMistakeStroke : "#a06868",
	downMistakeFill : "#601630",
	
	strokeWeight : 2,
	font : "Courier New",
	borderRad : 7
};

let canvasWidth = 720;
let canvasHeight = 480;

let keySize = 50;

let k = new Keyboard(keySize, defaultStyle);

function setup() {
	
	frameRate(60);
	createCanvas(canvasWidth, canvasHeight);
	
}

function draw() {
	
	background("#302030");
	
	k.update();
	k.draw(50, 50, defaultStyle);
	
}
