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