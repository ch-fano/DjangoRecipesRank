function viewStars(starRatingElement, rating) {
    const stars = starRatingElement.querySelectorAll('.star');

    const fullStars = Math.floor(rating);
    const fractionalPart = rating - fullStars;

    let partialClass = '';
    if (fractionalPart >= 0.75) {
        partialClass = 'three-quarters';
    } else if (fractionalPart >= 0.5) {
        partialClass = 'half';
    } else if (fractionalPart >= 0.25) {
        partialClass = 'quarter';
    }

    stars.forEach((star, index) => {
        star.classList.remove('full', 'half', 'quarter', 'three-quarters', 'empty');
        if (index < fullStars) {
            star.classList.add('full');
        } else if (index === fullStars && partialClass) {
            star.classList.add(partialClass);
        } else {
            star.classList.add('empty');
        }
    });
}