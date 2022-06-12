flip = (id) => {
    const inner = document.querySelector("#" + id + ">*");

    if (getComputedStyle(inner).transform == `matrix3d(-1, 0, 0, 0, 0, 1, 0, 0, 0, 0, -1, 0, 0, 0, 0, 1)`) {
        inner.style.transform = `rotateY(0deg)`;
    } else {
        inner.style.transform = `rotateY(180deg)`;
    }
}