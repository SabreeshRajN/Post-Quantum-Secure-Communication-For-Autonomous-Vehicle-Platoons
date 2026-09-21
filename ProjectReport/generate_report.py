import docx
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.style import WD_STYLE_TYPE
import fitz

def convert_pdf_to_image(pdf_path, img_path):
    doc = fitz.open(pdf_path)
    page = doc.load_page(0)
    pix = page.get_pixmap(dpi=300)
    pix.save(img_path)

def add_heading(doc, text, level=1, align=WD_ALIGN_PARAGRAPH.CENTER):
    h = doc.add_paragraph(text)
    h.alignment = align
    run = h.runs[0]
    run.font.name = 'Times New Roman'
    run.font.size = Pt(16)
    run.font.bold = True
    return h

def add_paragraph(doc, text, align=WD_ALIGN_PARAGRAPH.JUSTIFY, bold=False):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.line_spacing = 1.5
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(14)
    run.font.bold = bold
    return p

def main():
    convert_pdf_to_image("d:\\My Projects\\Capstone Project\\SystemArchitecture.pdf", "architecture.png")

    doc = docx.Document()
    
    # Setup styles
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Times New Roman'
    font.size = Pt(14)
    doc.styles['Normal'].paragraph_format.line_spacing = 1.5

    # --- Cover Page ---
    add_heading(doc, "POST-QUANTUM SECURE FIRMWARE DISTRIBUTION AND VEHICLE AUTHENTICATION USING CRYSTALS-DILITHIUM")
    doc.add_paragraph()
    add_heading(doc, "A PROJECT REPORT", level=2)
    doc.add_paragraph()
    add_paragraph(doc, "Submitted by", align=WD_ALIGN_PARAGRAPH.CENTER)
    
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("SABREESH RAJ N (Reg. No. 727823TUAM041)\nVARSHINI B M (Reg. No. 727823TUAM058)\nMOHAMMED SHAAHID A (Reg. No. 727823TUAM027)")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(14)
    r.font.italic = True
    r.font.bold = True

    doc.add_paragraph()
    add_paragraph(doc, "in partial fulfillment for the award of the degree\nof", align=WD_ALIGN_PARAGRAPH.CENTER)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("BACHELOR OF ENGINEERING\nin\nCOMPUTER SCIENCE AND ENGINEERING (ARTIFICIAL INTELLIGENCE AND MACHINE LEARNING)")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(14)
    r.font.italic = True

    doc.add_paragraph()
    doc.add_paragraph()
    add_heading(doc, "SRI KRISHNA COLLEGE OF TECHNOLOGY", level=3)
    add_paragraph(doc, "(An Autonomous Institution)\nAffiliated to Anna University and Approved by AICTE\nCoimbatore - 641 042", align=WD_ALIGN_PARAGRAPH.CENTER)
    add_heading(doc, "ANNA UNIVERSITY :: CHENNAI 600 025", level=3)
    add_heading(doc, "NOVEMBER 2026", level=3)
    doc.add_page_break()

    # --- Bonafide Certificate ---
    add_heading(doc, "SRI KRISHNA COLLEGE OF TECHNOLOGY")
    add_paragraph(doc, "(An Autonomous Institution)\nAffiliated to Anna University and Approved by AICTE\nKOVAIPUDUR, COIMBATORE - 641 042", align=WD_ALIGN_PARAGRAPH.CENTER)
    doc.add_paragraph()
    add_heading(doc, "BONAFIDE CERTIFICATE")
    add_paragraph(doc, "Certified that this project report \"POST-QUANTUM SECURE FIRMWARE DISTRIBUTION AND VEHICLE AUTHENTICATION USING CRYSTALS-DILITHIUM\" is the bonafide work of SABREESH RAJ N, VARSHINI B M and MOHAMMED SHAAHID A who carried out the project work under my supervision.")
    doc.add_paragraph()
    add_paragraph(doc, "SIGNATURE\t\t\t\t\tSIGNATURE\nDr. SUMA SIRA JACOB\t\t\t\tHEAD OF THE DEPARTMENT\nSUPERVISOR\nASSOCIATE PROFESSOR\nDepartment of CSE (AI/ML)\nSri Krishna College of Technology, Coimbatore - 641 042")
    doc.add_paragraph()
    add_paragraph(doc, "Submitted for the Project Viva-Voce Examination held on ________________.")
    add_paragraph(doc, "INTERNAL EXAMINER\t\t\tEXTERNAL EXAMINER")
    doc.add_page_break()

    # --- Declaration ---
    add_heading(doc, "DECLARATION")
    add_paragraph(doc, "We affirm that the project report titled \"POST-QUANTUM SECURE FIRMWARE DISTRIBUTION AND VEHICLE AUTHENTICATION USING CRYSTALS-DILITHIUM\" being submitted in partial fulfilment for the award of BACHELOR OF ENGINEERING in COMPUTER SCIENCE AND ENGINEERING (ARTIFICIAL INTELLIGENCE AND MACHINE LEARNING) is the original work carried out by us. It has not formed part of any other project report or dissertation on the basis of which a degree or award was conferred on an earlier occasion on this or any other candidate.")
    add_paragraph(doc, "Name\t\t\tReg. No.\t\tSignature\nSABREESH RAJ N\t727823TUAM041\t____________\nVARSHINI B M\t\t727823TUAM058\t____________\nMOHAMMED SHAAHID A\t727823TUAM027\t____________")
    add_paragraph(doc, "I certify that the declaration made by the above candidates is true to the best of my knowledge.")
    add_paragraph(doc, "Name and Signature of the Supervisor with Date: Dr. SUMA SIRA JACOB\n________________________________")
    doc.add_page_break()

    # --- Acknowledgement ---
    add_heading(doc, "ACKNOWLEDGEMENT")
    add_paragraph(doc, "With a grateful heart, we extend our sincere thanks to our Program Coordinator and Project Supervisor, Dr. Suma Sira Jacob, Assistant Professor, Department of Computer Science and Engineering (AI & ML), for her continuous motivation, constant guidance, constructive suggestions, and valuable support throughout the project. Her encouragement and insightful guidance greatly helped us enhance our knowledge, overcome challenges, and successfully complete our project.")
    doc.add_page_break()

    # --- Abstract ---
    add_heading(doc, "ABSTRACT")
    add_paragraph(doc, "Connected vehicles require low latency and secure communication links to be incorporated. But quantum computers with Shor algorithm can break the vehicular networks and the large security algorithms already in use, i.e., RSA, ECC and ECDSA. This article describes a quantum first-mover platooning communication in vehicles. We described our security framework using two of the four National Institute of Standards and Technologies (NIST) approved algorithms, CRYSTALS-Kyber (key encapsulation) and CRYSTALS-Dilithium (digital signatures). To keep the overhead of per-message overhead low in order to provide real-time platooning, we applied AES-256-GCM to stream all of the post-handshake traffic. The system set the following benchmarks: <4 millisecond (ms) key exchange, 1.13 ms average round trip time (RTT) and 35 ms latency (minimal and under the 100 ms platooning ceiling). As of now, the system can support 200 messages per second, key exchange success rate of 99.9 and a fail safe cutover of 200 ms. The main value of this research is to demonstrate the fact that compliance to quantum security does not affect the real-time operation in any aspect.")
    doc.add_page_break()

    # --- Table of Contents Placeholder ---
    add_heading(doc, "TABLE OF CONTENTS")
    add_paragraph(doc, "CHAPTER 1: INTRODUCTION\nCHAPTER 2: LITERATURE REVIEW\nCHAPTER 3: PROBLEM IDENTIFICATION\nCHAPTER 4: OBJECTIVE\nCHAPTER 5: PROBLEM SOLUTION\nCHAPTER 6: BLOCK DIAGRAM\nCHAPTER 7: METHODOLOGY\nCHAPTER 8: RESULTS AND DISCUSSION\nCHAPTER 9: CONCLUSION\nAPPENDICES\nSDG MAPPING\nREFERENCES")
    doc.add_page_break()

    # --- Chapters ---
    chapters = [
        ("CHAPTER 1", "INTRODUCTION", "1.1 Introduction\nThe modern intelligent transport systems harness the real-time V2V communication systems to coordinate vehicles in manners not possible with human drivers, such as formation shooting, cooperative braking, and collision warnings. Algorithms to secure such a communication link are an engineering marvel, but that they are being developed in a world with quantum computers, and to not-factorable-to-polynomial-time problems in the classical world is wanting.\n\n1.2 Conclusion\nIn this chapter, the fundamental need for post-quantum cryptographic security in autonomous vehicular networks was established, motivating the development of the proposed V2V platooning system."),
        ("CHAPTER 2", "LITERATURE REVIEW", "2.1 Introduction\nThis chapter discusses the existing security protocols in vehicular networks and their vulnerabilities to quantum attacks.\n\n2.2 Literature Survey\nThe trust model of vehicular communication systems based on the 802.11p standard and DSRC is identical to that of PKI-based systems. Even more basic is the fact that RSA and ECC have been shown to be broken by the algorithm of Shor, and so such systems are on a time-bomb. Numerous publications, which examine the underlying specific implementation of the PQC algorithms with respect to vehicles and transportations on lattices, have also appeared recently.\n\n2.3 Conclusion\nThe literature survey identifies a clear research gap: none of the published studies has utilized both CRYSTALS-Kyber and CRYSTALS-Dilithium in a live wireless testbed V2V at the same time."),
        ("CHAPTER 3", "PROBLEM IDENTIFICATION", "3.1 Introduction\nThis chapter outlines the specific problem addressed by this project.\n\n3.2 Problem Statement\nEnsuring the authenticity of communicating vehicles and the integrity of safety-critical messages remains a major challenge in autonomous vehicle platoon networks. As quantum computing threatens the security of classical digital signature algorithms, a quantum-resistant authentication mechanism is essential to establish trust and prevent unauthorized communication.\n\n3.3 Conclusion\nIdentifying the vulnerability of current V2V protocols to Shor's algorithm provides the foundational basis for implementing a robust post-quantum authentication framework."),
        ("CHAPTER 4", "OBJECTIVE", "4.1 Introduction\nThis chapter presents the main objectives of the proposed research.\n\n4.2 Objective\nTo develop a post-quantum authentication framework using CRYSTALS-Dilithium that ensures secure vehicle authentication, message integrity, and trusted communication in autonomous vehicle platoon networks.\n\n4.3 Conclusion\nThe objective ensures that the developed system will counteract quantum threats while maintaining the low-latency constraints required by platooning."),
        ("CHAPTER 5", "PROBLEM SOLUTION", "5.1 Introduction\nThis chapter explains the proposed cryptographic solution leveraging NIST-approved post-quantum algorithms.\n\n5.2 Solution Overview\nWe described our security framework using CRYSTALS-Kyber for key encapsulation and CRYSTALS-Dilithium for digital signatures. AES-256-GCM is applied to stream all post-handshake traffic to ensure real-time performance. A three-step authenticated handshake establishes the secure channel.\n\n5.3 Conclusion\nThe combination of Dilithium, Kyber, and AES-GCM offers a comprehensive solution that balances post-quantum security with real-time operational requirements."),
        ("CHAPTER 6", "BLOCK DIAGRAM", "6.1 Introduction\nThis chapter visualizes the architectural design of the proposed system.\n\n6.2 System Architecture\nThe system is built around a centralized leader that broadcasts driving commands to followers over UDP. It provides a secure channel establishing identity, preventing eavesdropping, tampering, impersonation, and replay attacks.\n"),
        ("CHAPTER 7", "METHODOLOGY", "7.1 Introduction\nThis chapter details the mathematical formulations and the stepwise operational methodology of the framework.\n\n7.2 Mathematical Formulation\nThe process of key pair generation of CRYSTALS-Kyber-768 lattice-based key pair is given by:\n(pk_k, sk_k) <- Kyber.KeyGen()\n\nThe CRYSTALS-Dilithium-3 key pair is generated by:\n(pk_d, sk_d) <- Dilithium.KeyGen()\n\nThe session key is derived as:\nK_session = KDF(K_shared || vid || vid_peer || T)\n\nThe AES-256-GCM encryption is given by:\nC = AES-GCM_{K_session}(m, IV)\ng = AuthTag(K_session, C, IV)\n\n7.3 Methodology\n1. Vehicle Registration: Generates Dilithium public/private key pairs and shares public keys.\n2. Message Authentication: Signs outgoing platoon messages using Dilithium private key.\n3. Signature Verification: Verifies received signatures using the sender's public key.\n\n7.4 Conclusion\nThe structured methodology ensures rigorous authentication and encrypted data transfer without violating the timing constraints of vehicle platooning."),
        ("CHAPTER 8", "RESULTS AND DISCUSSION", "8.1 Introduction\nThis chapter presents the empirical results obtained from testing the prototype system.\n\n8.2 Key Exchange and Latency\nThe system set the following benchmarks: <4 millisecond (ms) key exchange, 1.13 ms average round trip time (RTT) and 35 ms latency (minimal and under the 100 ms platooning ceiling). As of now, the system can support 200 messages per second, key exchange success rate of 99.9% and a fail-safe cutover of 200 ms.\n\n8.3 Conclusion\nThe results validate that compliance to quantum security does not compromise real-time operation in autonomous vehicle platoons."),
        ("CHAPTER 9", "CONCLUSION", "9.1 Introduction\nThis chapter summarizes the findings and outlines the future scope of the work.\n\n9.2 Conclusion\nThe proposed authentication framework addresses the need for quantum-resistant vehicle authentication in autonomous platoon networks using CRYSTALS-Dilithium. Experimental validation demonstrates successful signature generation and verification, effectively preventing message forgery and impersonation attacks. \n\n9.3 Future Scope\nPerformance under dedicated hardware for V2X radios, in dense multi-vehicle scenes, and under adversary channel conditions remains to be tested. These would be the next steps, along with acceleration for embedded systems using FPGAs/ASICS.\n\n9.4 Conclusion\nThis work establishes a robust foundation for trusted, quantum-secure autonomous vehicle communication in the post-quantum era.")
    ]

    for ch_num, ch_title, ch_content in chapters:
        add_heading(doc, ch_num)
        add_heading(doc, ch_title)
        for line in ch_content.split('\n'):
            if line.strip():
                if line[0].isdigit() and line[1] == '.':
                    add_paragraph(doc, line, bold=True, align=WD_ALIGN_PARAGRAPH.LEFT)
                else:
                    add_paragraph(doc, line)
        
        # Insert block diagram in Chapter 6
        if ch_num == "CHAPTER 6":
            try:
                doc.add_picture("architecture.png", width=Inches(6.0))
                add_paragraph(doc, "Fig. 1. System Architecture Flow (four layered decentralized design)", align=WD_ALIGN_PARAGRAPH.CENTER)
            except Exception as e:
                add_paragraph(doc, f"[Image rendering failed: {e}]")
            
            # Adding conclusion to chapter 6
            add_paragraph(doc, "6.3 Conclusion", bold=True, align=WD_ALIGN_PARAGRAPH.LEFT)
            add_paragraph(doc, "The architectural design effectively modularizes the application, control, security, and networking layers, facilitating a scalable V2V communication system.")
            
        doc.add_page_break()

    # --- SDG Mapping ---
    add_heading(doc, "SUSTAINABLE DEVELOPMENT GOALS MAPPING")
    add_paragraph(doc, "The Sustainable Development Goals are a collection of 17 global goals designed to blue print to achieve a better and more sustainable future for all. The SDGs, set in 2015 by the United Nations General Assembly and intended to be achieved by the year 2030, In 2015, 195 nations agreed as a blue print that they can change the world for the better. The project is based on one of the 17 goals.")
    
    add_paragraph(doc, "Which SDGs does the project directly address?", bold=True, align=WD_ALIGN_PARAGRAPH.LEFT)
    add_paragraph(doc, "SDG 9 - Industry, Innovation, and Infrastructure: Secure and resilient intelligent transportation systems.\nSDG 11 - Sustainable Cities and Communities: Improved road safety and reliable autonomous mobility.")
    
    add_paragraph(doc, "What strategies or actions are being implemented to achieve these goals?", bold=True, align=WD_ALIGN_PARAGRAPH.LEFT)
    add_paragraph(doc, "Indian Knowledge System (IKS) Integration:\nRaksha (Protection) : Proactive safeguarding of safety-critical transportation systems through quantum-resilient security.\nAnvikshiki (Scientific Inquiry) : Application of analytical reasoning and cryptographic innovation to solve emerging cybersecurity challenges.")
    doc.add_page_break()
    
    # --- References ---
    add_heading(doc, "REFERENCES")
    refs = [
        "C. Rubio García et al., \"Quantum-resistant Transport Layer Security,\" Computer Communications, vol. 213, pp. 345–358, 2024.",
        "G. Alagic et al., Status Report on the Third Round of the NIST Post-Quantum Cryptography Standardization Process, NIST SP 800-208A, 2022.",
        "N. Dottling et al., \"Post-Quantum Signatures from Dilithium,\" J. Cryptology, vol. 34, no. 2, pp. 1–45, 2021.",
        "H. Hartenstein and K. Laberteaux, \"A tutorial survey on vehicular ad hoc networks,\" IEEE Commun. Mag., vol. 46, no. 6, pp. 164–171, Jun. 2008.",
        "T. Kandappu et al., \"Quantum-Resistant V2V Communication: Challenges and Solutions,\" IEEE Trans. Veh. Technol., vol. 71, no. 4, pp. 3567–3580, 2022.",
        "H. Li et al., \"Lattice-Based Cryptography for Autonomous Vehicles,\" IEEE Access, vol. 11, pp. 45678–45692, 2023.",
        "D. J. Bernstein and T. Lange, \"Post-quantum cryptography,\" Nature, vol. 549, no. 7671, pp. 188–194, Sep. 2017."
    ]
    for ref in refs:
        add_paragraph(doc, ref, align=WD_ALIGN_PARAGRAPH.LEFT)

    doc.save("Project_Report.docx")
    print("Project_Report.docx successfully generated!")

if __name__ == "__main__":
    main()
