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
                "panel":"0px 0px 4px 0px #1E202940",   
            }
        }
    },

    plugins: []
};
