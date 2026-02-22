const faqItems = document.querySelectorAll('.faq-item');

faqItems.forEach(item => {
    item.addEventListener('click', () => {
        item.classList.toggle('active');
    });
});

function openTab(evt, tabName) {
    const tabLinks = document.getElementsByClassName("tab-link");
    const tabContent = document.getElementsByClassName("tab-content");

    for (let i = 0; i < tabContent.length; i++) {
        tabContent[i].classList.remove("active");
    }
    
    for (let i = 0; i < tabLinks.length; i++) {
        tabLinks[i].classList.remove("active");
    }

    document.getElementById(tabName).classList.add("active");
    evt.currentTarget.classList.add("active");
}


function openMenu() {
    document.getElementById('mobileMenuOverlay').classList.add('active');
    document.body.classList.add('menu-open');
    document.documentElement.classList.add('menu-open'); // <html>
}
function closeMenu() {
    document.getElementById('mobileMenuOverlay').classList.remove('active');
    document.body.classList.remove('menu-open');
    document.documentElement.classList.remove('menu-open');
}

// Handle all dropdown menus
const dropdowns = document.querySelectorAll('.dropdown');

dropdowns.forEach(dropdown => {
    const btn = dropdown.querySelector(".dropdown-btn");
    const menu = dropdown.querySelector(".dropdown-menu");

    // open / close when clicking the button
    btn.addEventListener("click", (e) => {
      e.stopPropagation();                 // don't trigger document click
      menu.classList.toggle("active");
    });

    // close when clicking anywhere else
    document.addEventListener("click", () => {
      menu.classList.remove("active");
    });
});