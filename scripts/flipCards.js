let state = [];

flip = (id) => {
    const inner = document.querySelector("#card_" + id + ">*");

    console.log(state);
    if (state[id] != 1) {
        inner.style.transform = `rotateY(180deg)`;
        state[id] = 1;
    } else {
        inner.style.transform = `rotateY(0deg)`;
        state[id] = 0;
    }
}