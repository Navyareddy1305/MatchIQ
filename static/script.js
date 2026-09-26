/* =========================================================
   MATCHIQ - AI WEBSITE INTERACTIONS
========================================================= */

document.addEventListener("DOMContentLoaded", () => {

    /* =====================================================
       SCROLL REVEAL
    ===================================================== */

    const revealElements = document.querySelectorAll(
        ".feature-card, .step, .stat, .section-heading, .cta-content"
    );

    revealElements.forEach((element) => {
        element.style.opacity = "0";
        element.style.transform = "translateY(25px)";
        element.style.transition =
            "opacity 0.7s ease, transform 0.7s ease";
    });


    const revealObserver = new IntersectionObserver(
        (entries, observer) => {

            entries.forEach((entry) => {

                if (!entry.isIntersecting) {
                    return;
                }

                entry.target.style.opacity = "1";
                entry.target.style.transform = "translateY(0)";

                observer.unobserve(entry.target);
            });

        },
        {
            threshold: 0.15
        }
    );


    revealElements.forEach((element) => {
        revealObserver.observe(element);
    });


    /* =====================================================
       ANIMATED COUNTERS
    ===================================================== */

    const counters = document.querySelectorAll(".stat strong");

    const animateCounter = (element) => {

        const originalText = element.textContent.trim();

        const match = originalText.match(
            /^([\d.]+)(.*)$/
        );

        if (!match) {
            return;
        }

        const target = parseFloat(match[1]);
        const suffix = match[2];

        let current = 0;

        const duration = 1400;

        const startTime = performance.now();


        const updateCounter = (currentTime) => {

            const elapsed = currentTime - startTime;

            const progress = Math.min(
                elapsed / duration,
                1
            );

            const eased =
                1 - Math.pow(1 - progress, 3);

            current = target * eased;


            if (target >= 1000) {

                element.textContent =
                    Math.floor(current / 1000) +
                    "K+" ;

            } else {

                element.textContent =
                    Math.floor(current) +
                    suffix;
            }


            if (progress < 1) {

                requestAnimationFrame(
                    updateCounter
                );

            } else {

                element.textContent =
                    originalText;
            }
        };


        requestAnimationFrame(
            updateCounter
        );
    };


    const counterObserver =
        new IntersectionObserver(
            (entries, observer) => {

                entries.forEach((entry) => {

                    if (!entry.isIntersecting) {
                        return;
                    }

                    animateCounter(entry.target);

                    observer.unobserve(entry.target);
                });

            },
            {
                threshold: 0.7
            }
        );


    counters.forEach((counter) => {
        counterObserver.observe(counter);
    });


    /* =====================================================
       AI CARD MOUSE MOVEMENT
    ===================================================== */

    const aiCard =
        document.querySelector(".ai-card");

    if (aiCard) {

        aiCard.addEventListener(
            "mousemove",
            (event) => {

                const rect =
                    aiCard.getBoundingClientRect();

                const x =
                    event.clientX - rect.left;

                const y =
                    event.clientY - rect.top;

                const centerX =
                    rect.width / 2;

                const centerY =
                    rect.height / 2;

                const rotateX =
                    ((y - centerY) / centerY) * -3;

                const rotateY =
                    ((x - centerX) / centerX) * 3;


                aiCard.style.transform =
                    `perspective(900px)
                     rotateX(${rotateX}deg)
                     rotateY(${rotateY}deg)
                     translateY(-4px)`;
            }
        );


        aiCard.addEventListener(
            "mouseleave",
            () => {

                aiCard.style.transform = "";

            }
        );
    }


    /* =====================================================
       BUTTON RIPPLE EFFECT
    ===================================================== */

    const buttons =
        document.querySelectorAll(
            ".primary-btn, .secondary-btn, .signup-btn"
        );


    buttons.forEach((button) => {

        button.addEventListener(
            "click",
            function (event) {

                const ripple =
                    document.createElement("span");

                const rect =
                    this.getBoundingClientRect();

                const size =
                    Math.max(
                        rect.width,
                        rect.height
                    );

                ripple.style.width =
                    `${size}px`;

                ripple.style.height =
                    `${size}px`;

                ripple.style.position =
                    "absolute";

                ripple.style.left =
                    `${event.clientX - rect.left - size / 2}px`;

                ripple.style.top =
                    `${event.clientY - rect.top - size / 2}px`;

                ripple.style.borderRadius =
                    "50%";

                ripple.style.background =
                    "rgba(255,255,255,0.25)";

                ripple.style.pointerEvents =
                    "none";

                ripple.style.transform =
                    "scale(0)";

                ripple.style.animation =
                    "matchiqRipple 0.6s ease-out";

                this.style.position =
                    "relative";

                this.style.overflow =
                    "hidden";

                this.appendChild(ripple);


                setTimeout(() => {
                    ripple.remove();
                }, 650);
            }
        );
    });


    /* =====================================================
       FLOATING AI PARTICLES
    ===================================================== */

    const hero =
        document.querySelector(".hero");


    if (hero) {

        const particleContainer =
            document.createElement("div");

        particleContainer.className =
            "ai-particles";


        hero.appendChild(
            particleContainer
        );


        for (let i = 0; i < 18; i++) {

            const particle =
                document.createElement("span");

            particle.className =
                "ai-particle";


            particle.style.left =
                `${Math.random() * 100}%`;

            particle.style.top =
                `${Math.random() * 100}%`;

            particle.style.animationDelay =
                `${Math.random() * 5}s`;

            particle.style.animationDuration =
                `${4 + Math.random() * 5}s`;


            particleContainer.appendChild(
                particle
            );
        }
    }


    /* =====================================================
       NAVBAR SCROLL EFFECT
    ===================================================== */

    const navbar =
        document.querySelector(".navbar");


    if (navbar) {

        window.addEventListener(
            "scroll",
            () => {

                if (window.scrollY > 30) {

                    navbar.style.boxShadow =
                        "0 15px 45px rgba(30,55,110,0.13)";

                    navbar.style.background =
                        "rgba(255,255,255,0.92)";

                } else {

                    navbar.style.boxShadow =
                        "0 15px 50px rgba(30,55,110,0.08)";

                    navbar.style.background =
                        "rgba(255,255,255,0.78)";
                }

            },
            {
                passive: true
            }
        );
    }


    /* =====================================================
       SMOOTH INTERNAL LINKS
    ===================================================== */

    document.querySelectorAll(
        'a[href^="#"]'
    ).forEach((link) => {

        link.addEventListener(
            "click",
            (event) => {

                const targetId =
                    link.getAttribute("href");

                if (
                    !targetId ||
                    targetId === "#"
                ) {
                    return;
                }


                const target =
                    document.querySelector(
                        targetId
                    );


                if (!target) {
                    return;
                }


                event.preventDefault();


                target.scrollIntoView({
                    behavior: "smooth",
                    block: "start"
                });
            }
        );
    });


    /* =====================================================
       AI STATUS ANIMATION
    ===================================================== */

    const recommendation =
        document.querySelector(
            ".recommendation p"
        );


    if (recommendation) {

        const messages = [

            "Add REST API and JavaScript experience to improve your match.",

            "Your Python experience is highly relevant to this role.",

            "Adding cloud experience could increase your match score.",

            "Your technical skills strongly align with this opportunity."

        ];


        let messageIndex = 0;


        setInterval(() => {

            recommendation.style.opacity =
                "0";


            setTimeout(() => {

                messageIndex =
                    (messageIndex + 1) %
                    messages.length;

                recommendation.textContent =
                    messages[messageIndex];

                recommendation.style.opacity =
                    "1";

            }, 350);

        }, 5000);


        recommendation.style.transition =
            "opacity 0.35s ease";
    }


    /* =====================================================
       SKILL HOVER EFFECT
    ===================================================== */

    const skills =
        document.querySelectorAll(
            ".skills span"
        );


    skills.forEach((skill) => {

        skill.addEventListener(
            "mouseenter",
            () => {

                skill.style.transform =
                    "translateY(-3px)";

                skill.style.boxShadow =
                    "0 7px 15px rgba(49,89,221,0.10)";

            }
        );


        skill.addEventListener(
            "mouseleave",
            () => {

                skill.style.transform =
                    "";

                skill.style.boxShadow =
                    "";

            }
        );
    });


    /* =====================================================
       PAGE LOADED
    ===================================================== */

    document.body.classList.add(
        "matchiq-loaded"
    );

});