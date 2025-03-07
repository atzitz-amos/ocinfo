let zIndex = 100;

function bindWindow(win) {
    /**
     *  bar */
    let bar = win.querySelector(".window-bar");
    bar.addEventListener("mousedown", ev => {
        let el = bar.parentElement;
        el.classList.add("dragging");

        let bbox = el.getBoundingClientRect();

        el.setAttribute("data-dragging-x", -bbox.x + ev.clientX);
        el.setAttribute("data-dragging-y", -bbox.y + ev.clientY);
    });
    bar.addEventListener("mouseup", ev => {
        bar.parentElement.classList.remove("dragging");
    });
    win.addEventListener("mousedown", ev => {
        win.style.zIndex = zIndex++;
    });
    /**
     * Buttons*/
    let close_button = win.querySelector(".window-close-option");
    close_button.addEventListener("click", ev => {
        win.remove();
    });
}

function bindTerminalToWindow(win, terminal) {
    /**
     * Input*/
    terminal.win = win;
    let command = win.querySelector(".command");
    command.addEventListener("keydown", ev => {
        if (ev.key === "Enter") {
            let cmd = command.value;
            command.value = "";
            invokeCommand(terminal, cmd)
        } else if (ev.key === "ArrowUp") {
            command.value = terminal.history[terminal.historyIndex] || "";
            terminal.historyIndex = Math.max(0, terminal.historyIndex - 1);
            window.setTimeout(() => command.setSelectionRange(command.value.length, command.value.length), 0);
        } else if (ev.key === "ArrowDown") {
            terminal.historyIndex = Math.min(terminal.history.length - 1, terminal.historyIndex + 1);
            command.value = terminal.history[terminal.historyIndex] || "";
            window.setTimeout(() => command.setSelectionRange(command.value.length, command.value.length), 0);
        }
    });

    win.addEventListener("click", ev => {
        command.focus();
    });
}

function openApp(app, x, y) {
    let appType = app.getAttribute("data-apptype");
    if (appType === "terminal") {
        openTerminalWindow("Modules", x + 20 + "px", y + 20 + "px");
    }
}

window.onload = () => {
    document.addEventListener("mousemove", ev => {
        let el = document.querySelector(".dragging");
        if (!el) return;

        let x = -parseInt(el.getAttribute("data-dragging-x")) + ev.clientX;
        let y = -parseInt(el.getAttribute("data-dragging-y")) + ev.clientY;

        el.style.left = x + "px";
        el.style.top = y + "px";

        el.offsetHeight;

        let bbox = el.getBoundingClientRect();
        let screenBbox = document.querySelector(".screen").getBoundingClientRect();

        if (bbox.right > screenBbox.width) {
            x -= (bbox.right - screenBbox.width);
        } else if (bbox.left < 0) {
            x -= (bbox.left);
        }
        if (bbox.bottom > screenBbox.height) {
            y -= (bbox.bottom - screenBbox.height);
        } else if (bbox.top < 0) {
            y -= (bbox.top);
        }

        el.style.left = x + "px";
        el.style.top = y + "px";
    });
    document.addEventListener("click", e => {
        if (e.target.classList.contains("app")) return;
        document.querySelectorAll(".selected").forEach(x => x.classList.remove("selected"));
    });

    document.querySelectorAll(".app").forEach(app => {
        app.addEventListener("mousedown", e => {
            document.querySelectorAll(".selected").forEach(x => x.classList.remove("selected"));
            app.classList.add("dragging", "selected")
            let bbox = app.getBoundingClientRect();
            app.setAttribute("data-dragging-x", -bbox.x + e.clientX);
            app.setAttribute("data-dragging-y", -bbox.y + e.clientY);
        });
        app.addEventListener("mouseup", e => {
            app.classList.remove("dragging");
        });

        app.addEventListener("dblclick", e => {
            console.log("dblclick");
            openApp(app, e.clientX, e.clientY);
        });
    });
    setTimeout(() => {
        document.querySelector(".screen").classList.add("welcoming");
        setTimeout(() => {
            document.querySelector(".screen").classList.remove("loading");
            document.querySelector(".welcome-screen").style.transitionDelay = "0s";
            document.querySelector(".welcome-screen").style.opacity = "0";
            document.querySelector(".window-loading-bar").style.opacity = "0";
            setTimeout(() => {
                const path = document.querySelector(".desktop-bg path");
                path.classList.add("d");
                document.querySelector(".desktop-bg").addEventListener("mouseenter", () => {
                    path.animate([
                        {
                            "strokeDashoffset": 300,
                            "fill": "transparent"
                        }, {
                            "fill": "transparent",
                            offset: 0.5
                        },
                        {
                            "strokeDashoffset": 0,
                            "fill": "white"
                        }
                    ], {"duration": 2000, "fill": "forwards", "easing": "ease-out"});
                });
            }, 1000);
        }, 2000);
    }, 2000);
};

const HELP_MSG = `<span class="help-header">Help [OCINF OS v1.0]:</span>

<table>
    <tr><td><span class="help-cmd">echo &lt;text&gt;</span></td><td>:</td><td><span class="help-text">Print text to terminal</span></td></tr>
    <tr><td><span class="help-cmd">clear</span></td><td>:</td><td><span class="help-text">Clear text</span></td></tr>
    <tr><td><span class="help-cmd">cd &lt;folder&gt;</span></td><td>:</td> <td><span class="help-text">Change directory</span></td></tr>
    <tr><td><span class="help-cmd">exit</span></td><td>:</td><td><span class="help-text">Close terminal</span></td></tr>
    <tr><td><span class="help-cmd">dir</span></td><td>:</td><td><span class="help-text">Show current content of folder</span></td></tr>
    <tr><td><span class="help-cmd">open &lt;file&gt;</span></td><td>:</td> <td><span class="help-text">Open a file</span></td></tr>
    <tr><td><span class="help-cmd">help</span></td><td>:</td><td><span class="help-text">Display this message</span></td></tr>
</table>
`;
const HEADER_TEXT = `/*
    Welcome to OCINF OS 1.0
    ------------------------

    Type 'help' for a list of available commands.
*/
                            `;

function openWindow(title, x = "20%", y = "20%") {
    let window = document.createElement("div");
    let bar = document.createElement("div");
    let content = document.createElement("div");
    let title_el = document.createElement("div");
    let options = document.createElement("div");
    let close_button = document.createElement("div");

    window.classList.add("window");
    bar.classList.add("window-bar");
    title_el.classList.add("window-title");
    options.classList.add("window-options");
    close_button.classList.add("window-close-option");
    close_button.classList.add("window-option");
    content.classList.add("window-content");

    title_el.textContent = title;
    close_button.textContent = "X";

    options.appendChild(close_button);
    bar.appendChild(title_el);
    bar.appendChild(options);
    window.appendChild(bar);
    window.appendChild(content);

    window.style.zIndex = zIndex++;
    window.style.left = x;
    window.style.top = y;

    document.querySelector(".screen").appendChild(window);
    bindWindow(window);
    return window;
}

function openTerminalWindow(loc = "Modules", x, y) {
    let win = openWindow("Terminal", x || "20%", y || "20%");
    win.classList.add("module");
    let terminal = document.createElement("div");
    let prompt = document.createElement("span");
    let header = document.createElement("pre");
    let input = document.createElement("div");
    let command = document.createElement("input");

    terminal.classList.add("terminal");
    prompt.classList.add("prompt");
    input.classList.add("terminal-input");
    header.classList.add("header");
    command.classList.add("command");

    header.textContent = HEADER_TEXT;
    prompt.textContent = `root@ocinf://${loc} $>`;

    terminal.appendChild(header);
    terminal.appendChild(input);
    input.appendChild(prompt);
    input.appendChild(command);

    const terminal_obj = {
        loc: loc, history: [], historyIndex: 0
    };
    terminal_obj.updateLoc = function (newLoc) {
        win.querySelector(".prompt").textContent = `root@ocinf://${newLoc} $>`;
        terminal_obj.loc = newLoc;
    }
    setTimeout(() => bindTerminalToWindow(win, terminal_obj), 0);

    win.querySelector(".window-content").appendChild(terminal);
}

function openExerciseWindow(fileData, x, y) {
    console.log(fileData);

    let win = openWindow(fileData.id.toUpperCase(), x + "px", y + "px");
    let header = document.createElement("div");
    let span1 = document.createElement("span");
    let span2 = document.createElement("span");
    let main = document.createElement("div");
    let previewLink = document.createElement("a");
    let preview = document.createElement("div");
    let iframe = document.createElement("iframe");
    let svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    let path = document.createElementNS("http://www.w3.org/2000/svg", "path");

    win.classList.add("exercise");

    header.classList.add("exercise-header");
    span2.classList.add("n");
    main.classList.add("exercise-main");
    previewLink.classList.add("preview-link");
    preview.classList.add("exercise-preview");
    iframe.classList.add("preview-iframe");
    svg.classList.add("open-icon");

    span1.textContent = fileData.name.toUpperCase();
    span2.textContent = fileData.id.slice(2);

    previewLink.href = `./${fileData.module}/${fileData.module}_${fileData.id}.html`;
    previewLink.target = "_blank";

    iframe.src = `./${fileData.module}/${fileData.module}_${fileData.id}.html`;
    iframe.setAttribute("sandbox", "allow-same-origin");

    svg.setAttribute("viewBox", "0 0 24 24");
    path.setAttribute("d", "M10.0002 5H8.2002C7.08009 5 6.51962 5 6.0918 5.21799C5.71547 5.40973 5.40973 5.71547 5.21799 6.0918C5 6.51962 5 7.08009 5 8.2002V15.8002C5 16.9203 5 17.4801 5.21799 17.9079C5.40973 18.2842 5.71547 18.5905 6.0918 18.7822C6.5192 19 7.07899 19 8.19691 19H15.8031C16.921 19 17.48 19 17.9074 18.7822C18.2837 18.5905 18.5905 18.2839 18.7822 17.9076C19 17.4802 19 16.921 19 15.8031V14M20 9V4M20 4H15M20 4L13 11");

    header.appendChild(span1);
    header.appendChild(span2);
    svg.appendChild(path);
    preview.appendChild(iframe);
    preview.appendChild(svg);
    previewLink.appendChild(preview);
    main.appendChild(previewLink);

    win.querySelector(".window-content").appendChild(header);
    win.querySelector(".window-content").appendChild(main);
}

const commands = {
    echo: function (cmd, terminal, args) {
        args = args.join(" ");
        this.write(args, terminal, true);
    }, clear: function (cmd, terminal, args) {
        terminal.win.querySelectorAll(".output-prompt").forEach(el => el.remove());
        terminal.win.querySelectorAll(".output").forEach(el => el.remove());
    }, help: function (cmd, terminal, args) {
        if (!args.length || args.length === 0) {
            this.write(HELP_MSG, terminal)
        }
    }, dir: function (cmd, terminal, args) {
        if (terminal.loc === "Modules") {
            let output = "";
            MODULES.forEach(module => {
                output += `<span class="dir-file-type">&lt;DIR&gt;</span><span class="dir-file">${module.name}</span><span class="dir-name">${module.name}</span><br>`;
            });
            this.write(output, terminal, false, "dir");
            return;
        }
        let data = MODULES.find(x => x.name === terminal.loc.slice("Modules/".length));
        if (!data) {
            this.write("No files", terminal)
            return;
        }
        let files = data.exercises;
        let output = "<table>";
        files.forEach(file => {
            output += `<tr><td><span class="dir-file-type">&lt;FILE&gt;</span></td><td><span class="dir-file">${file.id}</span></td><td><span class="dir-name">${file.name}</span></td>`;
        });
        this.write(output + "</table>", terminal, false, "dir");

    }, cd: function (cmd, terminal, args) {
        let module = args[0];
        if (!module) {
            this.error("No directory specified", terminal);
            return;
        }
        if (module.startsWith("/")) {
            module = module.slice(1);
        }
        if (module.startsWith("..")) {
            terminal.updateLoc("Modules");
            if (module.charAt(2) === "/") {
                this.cd(cmd, terminal, [module.slice(2)]);
            }
            return;
        }
        if (terminal.loc !== "Modules") {
            this.error(`No such directory: ${module}`, terminal);
            return;
        }
        let data = MODULES.find(x => x.name === module);
        if (!data) {
            this.error(`No such directory: ${module}`, terminal);
            return;
        }
        terminal.updateLoc(`Modules/${module}`);
    }, exit: function (cmd, terminal, args) {
        terminal.win.remove();
    }, open: function (cmd, terminal, args) {
        let file = args[0];
        if (!file) {
            this.error("No file specified", terminal);
            return;
        }
        let file2 = file;
        if (file2.startsWith(".")) {
            file2 = file2.slice(1);
        }
        if (file2.startsWith("/")) {
            file2 = file2.slice(1);
        }
        let data = MODULES.find(x => x.name === terminal.loc.slice("Modules/".length));
        if (!data) {
            this.error(`File not found: '${file}'`, terminal);
            return;
        }
        let fileData = data.exercises.find(x => x.id === file2);
        if (!fileData) {
            this.error(`File not found: '${file}'`, terminal);
            return;
        }
        fileData["module"] = data.name;

        let bbox = terminal.win.getBoundingClientRect();
        openExerciseWindow(fileData, bbox.x + 70, bbox.y + 70);
    },
    error: function (msg, terminal) {
        this.write(msg, terminal, true, "error");
    }, write: function (msg, terminal, safe = false, className = null) {
        let output = document.createElement("div");
        output.classList.add("output");
        className && output.classList.add(className);

        safe ? (output.textContent = msg) : (output.innerHTML = msg);

        terminal.win.querySelector(".terminal").insertBefore(output, terminal.win.querySelector(".terminal-input"));
    }
}

function invokeCommand(terminal, cmd) {
    let terminalinput = terminal.win.querySelector(".terminal-input");
    let command = cmd.split(" ");
    let commandName = command[0];
    let args = command.slice(1);

    let prompt = document.createElement("div");
    let command_el = document.createElement("span");
    command_el.classList.add("command");
    prompt.classList.add("output-prompt");
    prompt.textContent = terminal.win.querySelector(".prompt").textContent + " ";
    command_el.textContent = cmd;
    prompt.appendChild(command_el);
    terminal.win.querySelector(".terminal").insertBefore(prompt, terminalinput);

    if (cmd.startsWith("./")) {
        commands.open(cmd, terminal, [cmd.slice(2)]);
    } else {
        switch (commandName) {
            case "":
                break;
            case "echo":
                commands.echo(cmd, terminal, args)
                break;
            case "exit":
                commands.exit(cmd, terminal, args);
                break;
            case "dir":
                commands.dir(cmd, terminal, args);
                break;
            case "cd":
                commands.cd(cmd, terminal, args);
                break;
            case "open":
                commands.open(cmd, terminal, args);
                break;
            case "clear":
                commands.clear(cmd, terminal, args);
                break;
            case "help":
                commands.help(cmd, terminal, args);
                break;
            default:
                commands.error("Unknown command: '" + commandName + "', type 'help' for more information", terminal);
                break;
        }
    }
    if (cmd !== "") {
        terminal.history.push(cmd);
        terminal.historyIndex = terminal.history.length - 1;
    }
    terminalinput.scrollIntoView({block: "nearest"});
}





