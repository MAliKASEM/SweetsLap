document.addEventListener('DOMContentLoaded', () => {
    // 1. Progressive Image Lazy Loading
    const lazyImages = document.querySelectorAll('.menu-image');
    
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const image = entry.target;
                    const realSrc = image.dataset.src;
                    
                    if (realSrc) {
                        image.src = realSrc;
                        image.onload = () => {
                            image.classList.add('loaded');
                            const wrapper = image.closest('.image-wrapper');
                            if (wrapper) {
                                wrapper.classList.remove('skeleton');
                            }
                        };
                    }
                    imageObserver.unobserve(image);
                }
            });
        }, {
            rootMargin: '50px 0px', // Start loading slightly before coming into view
            threshold: 0.01
        });
        
        lazyImages.forEach(image => imageObserver.observe(image));
    } else {
        // Fallback for older browsers
        lazyImages.forEach(image => {
            const realSrc = image.dataset.src;
            if (realSrc) {
                image.src = realSrc;
                image.onload = () => {
                    image.classList.add('loaded');
                    const wrapper = image.closest('.image-wrapper');
                    if (wrapper) {
                        wrapper.classList.remove('skeleton');
                    }
                };
            }
        });
    }

    // 2. Category Filter Interaction
    const filterButtons = document.querySelectorAll('.filter-btn');
    const drinkGroup = document.getElementById('group-drink');
    const dessertGroup = document.getElementById('group-dessert');
    
    filterButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            // Remove active class from all buttons
            filterButtons.forEach(b => b.classList.remove('active'));
            // Add active class to clicked button
            btn.classList.add('active');
            
            const filter = btn.dataset.filter;
            
            // Add fade transition
            const fadeOut = (el) => {
                el.style.opacity = '0';
                setTimeout(() => {
                    el.style.display = 'none';
                }, 300);
            };
            
            const fadeIn = (el) => {
                el.style.display = 'block';
                setTimeout(() => {
                    el.style.opacity = '1';
                }, 50);
            };
            
            // Apply CSS transitions dynamically
            [drinkGroup, dessertGroup].forEach(g => {
                if (g) {
                    g.style.transition = 'opacity 0.3s ease';
                }
            });
            
            if (filter === 'all') {
                fadeIn(drinkGroup);
                fadeIn(dessertGroup);
            } else if (filter === 'drink') {
                fadeIn(drinkGroup);
                fadeOut(dessertGroup);
            } else if (filter === 'dessert') {
                fadeOut(drinkGroup);
                fadeIn(dessertGroup);
            }
        });
    });
});
