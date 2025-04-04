import ctypes
import sys
from ctypes import wintypes

# Windows API constants
DEBUG_PROCESS = 0x00000001
CREATE_NEW_CONSOLE = 0x00000010
DBG_CONTINUE = 0x00010002
EXCEPTION_DEBUG_EVENT = 1
EXCEPTION_SINGLE_STEP = 0x80000004


# Define necessary Windows structures
class STARTUPINFO(ctypes.Structure):
    _fields_ = [
        ("cb", wintypes.DWORD),
        ("lpReserved", wintypes.LPSTR),
        ("lpDesktop", wintypes.LPSTR),
        ("lpTitle", wintypes.LPSTR),
        ("dwX", wintypes.DWORD),
        ("dwY", wintypes.DWORD),
        ("dwXSize", wintypes.DWORD),
        ("dwYSize", wintypes.DWORD),
        ("dwXCountChars", wintypes.DWORD),
        ("dwYCountChars", wintypes.DWORD),
        ("dwFillAttribute", wintypes.DWORD),
        ("dwFlags", wintypes.DWORD),
        ("wShowWindow", wintypes.WORD),
        ("cbReserved2", wintypes.WORD),
        ("lpReserved2", ctypes.POINTER(ctypes.c_ubyte)),
        ("hStdInput", wintypes.HANDLE),
        ("hStdOutput", wintypes.HANDLE),
        ("hStdError", wintypes.HANDLE),
    ]


class PROCESS_INFORMATION(ctypes.Structure):
    _fields_ = [
        ("hProcess", wintypes.HANDLE),
        ("hThread", wintypes.HANDLE),
        ("dwProcessId", wintypes.DWORD),
        ("dwThreadId", wintypes.DWORD),
    ]


class CONTEXT(ctypes.Structure):
    _fields_ = [
        ("ContextFlags", wintypes.DWORD),
        ("Dr0", wintypes.DWORD),
        ("Dr1", wintypes.DWORD),
        ("Dr2", wintypes.DWORD),
        ("Dr3", wintypes.DWORD),
        ("Dr6", wintypes.DWORD),
        ("Dr7", wintypes.DWORD),
        ("FloatSave", wintypes.BYTE * 512),
        ("SegGs", wintypes.DWORD),
        ("SegFs", wintypes.DWORD),
        ("SegEs", wintypes.DWORD),
        ("SegDs", wintypes.DWORD),
        ("Edi", wintypes.DWORD),
        ("Esi", wintypes.DWORD),
        ("Ebx", wintypes.DWORD),
        ("Edx", wintypes.DWORD),
        ("Ecx", wintypes.DWORD),
        ("Eax", wintypes.DWORD),
        ("Ebp", wintypes.DWORD),
        ("Eip", wintypes.DWORD),
        ("SegCs", wintypes.DWORD),
        ("EFlags", wintypes.DWORD),
        ("Esp", wintypes.DWORD),
        ("SegSs", wintypes.DWORD),
    ]


class DEBUG_EVENT(ctypes.Structure):
    _fields_ = [
        ("dwDebugEventCode", wintypes.DWORD),
        ("dwProcessId", wintypes.DWORD),
        ("dwThreadId", wintypes.DWORD),
        ("u", wintypes.BYTE * 1024),  # Placeholder for event-specific data
    ]


# Load Windows API functions
kernel32 = ctypes.windll.kernel32
CreateProcess = kernel32.CreateProcessA
WaitForDebugEvent = kernel32.WaitForDebugEvent
ContinueDebugEvent = kernel32.ContinueDebugEvent
GetThreadContext = kernel32.GetThreadContext
SetThreadContext = kernel32.SetThreadContext


# Function to start and attach debugger to a process
def start_process(path):
    si = STARTUPINFO()
    si.cb = ctypes.sizeof(STARTUPINFO)
    pi = PROCESS_INFORMATION()

    success = CreateProcess(
        path.encode('utf-8'), None, None, None, False,
        DEBUG_PROCESS | CREATE_NEW_CONSOLE, None, None,
        ctypes.byref(si), ctypes.byref(pi)
    )

    if success:
        print(f"[*] Started process: {pi.dwProcessId}")
        return pi
    else:
        print("[-] Failed to start process")
        sys.exit(1)


# Function to enable the Trap Flag (TF)
def set_trap_flag(pi):
    context = CONTEXT()
    context.ContextFlags = 0x10007  # CONTEXT_FULL

    if GetThreadContext(pi.hThread, ctypes.byref(context)):
        context.EFlags |= 0x100  # Set Trap Flag (TF)
        SetThreadContext(pi.hThread, ctypes.byref(context))
        print("[*] Trap Flag set. Single-stepping enabled!")
    else:
        print("[-] Failed to set Trap Flag")


# Function to listen for debug events
def debug_loop(pi):
    debug_event = DEBUG_EVENT()

    while True:
        if WaitForDebugEvent(ctypes.byref(debug_event), 100):  # 100ms timeout
            if debug_event.dwDebugEventCode == EXCEPTION_DEBUG_EVENT:
                print(f"[*] Exception at PID {debug_event.dwProcessId}")

                # Handle single-step event
                context = CONTEXT()
                context.ContextFlags = 0x10007  # CONTEXT_FULL

                if GetThreadContext(pi.hThread, ctypes.byref(context)):
                    print(f"EIP: {hex(context.Eip)} | EAX: {hex(context.Eax)} | EBX: {hex(context.Ebx)}")

                    # Re-enable Trap Flag for next instruction
                    context.EFlags |= 0x100
                    SetThreadContext(pi.hThread, ctypes.byref(context))

            # Continue execution
            ContinueDebugEvent(debug_event.dwProcessId, debug_event.dwThreadId, DBG_CONTINUE)


# Main function
def main():
    target_exe = "./test.exe"
    pi = start_process(target_exe)

    # Enable single-step mode
    set_trap_flag(pi)

    # Start debugging loop
    debug_loop(pi)


if __name__ == "__main__":
    main()
