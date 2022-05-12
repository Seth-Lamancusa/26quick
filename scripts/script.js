class key {
	
	constructor (w, h, content, optArgs) {
		this.w = w;
		this.h = h;
		this.content = content;
		
		this.color = ("color" in optArgs) ? this.color = optArgs[color] : this.color = 200;
		
	}
	
}





class Keyboard {
	
	constructor(keySize) {
		
		this.state = 0;
		this.time = 0;
		this.mistakes = 0;
		this.keySize = keySize;
		this.altKeySize = this.keySize * 1.3;
		
		this.keyUpColor = 200;
		this.keyDownColor = 100;
		this.mistakeColor = "#ff0000";
		this.mistakeDownColor = "#884444";
		
		this.isDown = new Array(28);
		this.prevDown = new Array(28);
		
		this.keyColors = new Array(26);
		this.keyColors.fill(this.keyUpColor);
		this.pressed = new Array(26);
		this.pressed.fill(false);
		this.immune = new Array(26);
		this.immune.fill(false);
		this.keyContent = new Array(28);
		this.keyContent.fill('');
		
		this.keyContent[13] = '1';
		this.keyContent[14] = '-';
		this.keyContent[15] = '2';
		this.keyContent[16] = '6';
		
		this.expectedNext = 1;
		
	}
	
	static drawKey(kbX, kbY, w, h, offsetX, offsetY, content, color) {
		
		noFill();
		strokeWeight(2);
		stroke(color);
		rect(kbX + offsetX, kbY + offsetY, w, h, 7);
		
		textSize(keySize / 2);
		textFont("Courier New");
		textAlign(CENTER, CENTER);
		text(content, kbX + offsetX + w / 2, kbY + offsetY + h / 2);
		
	}
	
	static shuffle(array) {
		let currentIndex = array.length, randomIndex;
		
		/* This is from StackOverflow and I don't know how it works. */
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
		this.keyContent = numbers;
	}
	
	draw(x, y) {
		
		let rowOffsets = [0, 2 * this.keySize / 7, this.keySize, this.keySize * 1.6];
		
		/* draws row 1 of letter keys */
		for (let i = 0; i < 10; i++) {
			Keyboard.drawKey(x, y, this.keySize, this.keySize, 
				rowOffsets[0] + i * (this.keySize + this.keySize / 7), 0, 
				this.keyContent[i], this.keyColors[i]);
		}
		/* draws row 2 of letter keys */
		for (let i = 0; i < 9; i++) {
			Keyboard.drawKey(x, y, this.keySize, this.keySize, 
				rowOffsets[1] + i * (this.keySize + this.keySize / 7), this.keySize + this.keySize / 7, 
				this.keyContent[10 + i], this.keyColors[10 + i]);
		}
		/* draws row 3 of letter keys */
		for (let i = 0; i < 7; i++) {
			Keyboard.drawKey(x, y, this.keySize, this.keySize, 
				rowOffsets[2] + i * (this.keySize + this.keySize / 7), 2 * (this.keySize + this.keySize / 7), 
				this.keyContent[19 + i], this.keyColors[19 + i]);
		}
		
		/* draws space bar */
		this.keyContent[27] = this.state == 0 ? "start" : (Math.round(this.time / 60 * 100) / 100).toFixed(2);
		Keyboard.drawKey(x, y, (this.keySize + this.keySize / 7) * 6, this.keySize,
			rowOffsets[3] + this.altKeySize + this.keySize / 7, 3 * (this.keySize + this.keySize / 7),
			this.keyContent[27], this.keyUpColor);
		
		/* draws left alt */
		this.keyContent[28] = this.mistakes;
		Keyboard.drawKey(x, y, this.altKeySize, this.keySize,
			rowOffsets[3], 3 * (this.keySize + this.keySize / 7),
			this.keyContent[28], this.keyUpColor);
	
	}
	
	update(inputs) {
		
		this.prevDown = this.isDown;
		this.isDown = inputs;
		
		
		switch (this.state) {
			case 0:
			
				if (this.isDown[26]) {
					this.start();
				}
				
				break;
			case 1:
			
				this.time++;
				for (let i = 0; i < 26; i++) {
					if (this.isDown[i]) {
						if (this.keyContent[i] == this.expectedNext) {
							this.pressed[i] = true;
							this.immune[i] = true;
							this.keyColors[i] = this.keyDownColor;
							this.expectedNext++;
						} else if (!this.immune[i]) {
							this.keyColors[i] = this.pressed[i] ? this.mistakeDownColor : this.mistakeColor;
							if (!this.prevDown[i]) {
								this.mistakes++;	
							}
						}
					} else {
						this.keyColors[i] = this.pressed[i] ? this.keyDownColor : this.keyUpColor;
						this.immune[i] = false;
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





let canvasWidth = 720;
let canvasHeight = 480;

let keySize = 50;

let k = new Keyboard(keySize, 50, 50);

let inputs;

function setup() {
	
	frameRate(60);
	createCanvas(canvasWidth, canvasHeight);
	
}

function draw() {

	background(50, 20, 50);
	
	inputs = getUserInput();
	
	k.update(inputs);
	k.draw(50, 50);
	
}



function getUserInput() {
	
	let keycodes = [81, 87, 69, 82, 84, 89, 85, 73, 79, 80, 65, 83, 68, 70, 71, 72, 74, 75, 76, 90, 88, 67, 86, 66, 78, 77, 32];
	let inputs = new Array(27);
	inputs.fill(false);
	
	for (let i = 0; i < 27; i++) {
		if (keyIsDown(keycodes[i])) {
			inputs[i] = true;
		}
	}
	
	return inputs;
	
}
