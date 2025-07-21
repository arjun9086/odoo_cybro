/** @odoo-module **/
import { registry } from "@web/core/registry";
import { Component, useState, useRef } from "@odoo/owl";

class SystrayQrcode extends Component {
    setup() {
        this.state = useState({
            inputText: "",
            qrcodeUrl: "",
            isVisible: false,
        });
        this.hiddenQRRef = useRef("hiddenQR");
    }
    togglePopover() {
        this.state.isVisible = !this.state.isVisible;
    }
    generateQR() {
        const text = this.state.inputText.trim();
        if (!text) {
            alert("No input text to generate QR");
            return;
        }
        const container = this.hiddenQRRef.el;
        if (!container) {
            alert("QR container not found");
            return;
        }
        container.innerHTML = "";
        const qr = new QRCode(container, {
            text: text,
            width: 250,
            height: 250,
        });
        setTimeout(() => {
        const canvas = container.firstElementChild;
        if (canvas && canvas.tagName === "CANVAS") {
            this.state.qrcodeUrl = canvas.toDataURL("image/png");
        } else {
            console.error("QR generation failed: canvas not found");
        }
    }, 200);
//        setTimeout(() => {
//            const canvas = container.querySelector("canvas");
//            if (canvas) {
//                this.state.qrcodeUrl = canvas.toDataURL("image/png");
//            } else {
//                console.error("QR generation failed: canvas not found");
//            }
//        }, 200);
    }
    reset() {
        this.state.inputText = "";
        this.state.qrcodeUrl = "";
        const container = this.hiddenQRRef.el;
        if (container) {
            container.innerHTML = "";
        }
    }
    downloadQR() {
        if (!this.state.qrcodeUrl) return;
        const link = document.createElement("a");
        link.href = this.state.qrcodeUrl;
        link.download = "qrcode.png";
        link.click();
    }
}
SystrayQrcode.template = "systray_qrcode";
export const systrayItem = {
    Component: SystrayQrcode,
};
registry.category("systray").add("systray_qrcode",systrayItem,{ sequence: 1 });
export default SystrayQrcode;


///** @odoo-module **/
//
//import { registry } from "@web/core/registry";
//import { Component, useRef, useState, onMounted } from "@odoo/owl";
//import { loadJS } from "@web/core/assets";
//
//class SystrayQrcode extends Component {
//    setup() {
//        this.state = useState({
//            inputText: "",
//            isVisible: false,
//            qrReady: false,
//        });
//
//        this.qrContainerRef = useRef("qrContainer");
//        this.qrCanvasData = null;
//
//
//    }
//    togglePopover() {
//        this.state.isVisible = !this.state.isVisible;
//        if (!this.state.isVisible) {
//            this.reset();
//        }
//    }
//    generateQR() {
//        const container = this.qrContainerRef.el;
//        const text = this.state.inputText.trim();
//        if (!text) {
//            alert("Please enter some text");
//            return;
//        }
//
//        container.innerHTML = ""; // Safe here; we control this element
//        const qr = new QRCode(container, {
//            text: text,
//            width: 250,
//            height: 250,
//            correctLevel: QRCode.CorrectLevel.H,
//        });
//
//        // Let QRCode library render, then fetch canvas via ref's children
//        setTimeout(() => {
//            const canvas = Array.from(container.children).find(child => child.tagName === 'CANVAS');
//            if (canvas) {
//                this.qrCanvasData = canvas.toDataURL("image/png");
//                this.state.qrReady = true;
//            }
//        }, 100);
//    }
//
//    reset() {
//        this.state.inputText = "";
//        this.state.qrReady = false;
//        this.qrCanvasData = null;
//        const container = this.qrContainerRef.el;
//        container.innerHTML = "";
//    }
//
//    downloadQR() {
//        if (!this.qrCanvasData) return;
//        const link = document.createElement("a");
//        link.href = this.qrCanvasData;
//        link.download = "qrcode.png";
//        link.click();
//    }
//}
//
//SystrayQrcode.template = "systray_qrcode";
//
//export const systrayItem = {
//    Component: SystrayQrcode,
//};
//registry.category("systray").add("systray_qrcode", systrayItem, { sequence: 1 });
//export default SystrayQrcode;

