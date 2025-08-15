document.getElementById("openLogin").onclick = () => {
  document.getElementById("loginModal").style.display = "block";
};

document.getElementById("openSignup").onclick = () => {
  document.getElementById("signupModal").style.display = "block";
};

document.querySelectorAll(".close").forEach(closeBtn => {
  closeBtn.onclick = () => {
    document.getElementById(closeBtn.dataset.close).style.display = "none";
  };
});

window.onclick = (event) => {
  document.querySelectorAll(".modal").forEach(modal => {
    if (event.target === modal) {
      modal.style.display = "none";
    }
  });
};
