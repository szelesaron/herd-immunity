if (/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) {
    // redirect to the mobile-html
    document.location = "../templates/mobile-view.html";
} 