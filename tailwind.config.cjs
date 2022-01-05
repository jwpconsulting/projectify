module.exports = {
    mode: "jit",
    purge: ["./src/**/*.svelte"],
    content: ["./src/**/*.{html,js,svelte,ts}"],

    theme: {
        colors: {
            "wite-1": "#FFFFFF",
            "border-1": "#A6B2B7",
            "black-1": "#002332",    
            "black-2": "#326478",    
            "black-3": "#78A0B0",    
            "black-4": "#BED2DC",    
            "blue-1": "#00A0EB",
            "blue-2": "#67CDFA",
            "blue-3": "#F0F5FF",
            "dark-blue-1": "#006491",  
            "yellow-1": "#FFF56B",
        },
        extend: {
            boxShadow:{
                "card":"0px 0px 4px 0px #1E202940",   
            }
        }
    },

    plugins: [
        require('@tailwindcss/typography'),
        require('daisyui'),
    ],

    daisyui: {
        styled: true,
        themes: [
            {
                "app-light":{
                    'primary' : '#00A0EB',           /* Primary color */
                    'primary-focus' : '#67CDFA',     /* Primary color - focused */
                    'primary-content' : '#ffffff',   /* Foreground content color to use on primary color */
         
                    'secondary' : '#f6d860',         /* Secondary color */
                    'secondary-focus' : '#f3cc30',   /* Secondary color - focused */
                    'secondary-content' : '#ffffff', /* Foreground content color to use on secondary color */
         
                    'accent' : '#37cdbe',            /* Accent color */
                    'accent-focus' : '#2aa79b',      /* Accent color - focused */
                    'accent-content' : '#ffffff',    /* Foreground content color to use on accent color */
         
                    'neutral' : '#3d4451',           /* Neutral color */
                    'neutral-focus' : '#2a2e37',     /* Neutral color - focused */
                    'neutral-content' : '#ffffff',   /* Foreground content color to use on neutral color */
         
                    'base-100' : '#ffffff',          /* Base color of page, used for blank backgrounds */
                    'base-200' : '#f9fafb',          /* Base color, a little darker */
                    'base-300' : '#d1d5db',          /* Base color, even more darker */
                    'base-content' : '#1f2937',      /* Foreground content color to use on base color */
         
                    'info' : '#2094f3',              /* Info */
                    'success' : '#009485',           /* Success */
                    'warning' : '#ff9900',           /* Warning */
                    'error' : '#ff5724',             /* Error */
                },
            }
        ]
    },
};
