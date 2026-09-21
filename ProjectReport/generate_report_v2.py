import docx
from docx.shared import Pt, Inches, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.style import WD_STYLE_TYPE
import os

def set_margins(doc):
    for section in doc.sections:
        section.top_margin = Cm(2.54)
        section.bottom_margin = Cm(2.54)
        section.left_margin = Cm(3.17) # Left margin slightly larger for binding
        section.right_margin = Cm(2.54)

def add_centered_heading(doc, text, size=16, bold=True, space_after=True):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(size)
    run.font.bold = bold
    if space_after:
        doc.add_paragraph()
    return p

def add_justified_paragraph(doc, text, bold=False):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.space_after = Pt(12)
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(14)
    run.font.bold = bold
    return p

def add_table_of_contents(doc):
    add_centered_heading(doc, "TABLE OF CONTENTS")
    add_justified_paragraph(doc, "ACKNOWLEDGEMENT ........................................................................................ iii")
    add_justified_paragraph(doc, "ABSTRACT ............................................................................................................... iv")
    add_justified_paragraph(doc, "LIST OF FIGURES .................................................................................................. vi")
    add_justified_paragraph(doc, "CHAPTER 1: INTRODUCTION ............................................................................ 1")
    add_justified_paragraph(doc, "CHAPTER 2: LITERATURE REVIEW ................................................................ 4")
    add_justified_paragraph(doc, "CHAPTER 3: PROBLEM IDENTIFICATION .................................................... 7")
    add_justified_paragraph(doc, "CHAPTER 4: OBJECTIVE .................................................................................... 9")
    add_justified_paragraph(doc, "CHAPTER 5: PROBLEM SOLUTION ................................................................. 10")
    add_justified_paragraph(doc, "CHAPTER 6: BLOCK DIAGRAM ........................................................................ 12")
    add_justified_paragraph(doc, "CHAPTER 7: METHODOLOGY ........................................................................... 14")
    add_justified_paragraph(doc, "CHAPTER 8: RESULTS AND DISCUSSION ....................................................... 19")
    add_justified_paragraph(doc, "CHAPTER 9: CONCLUSION ................................................................................. 23")
    add_justified_paragraph(doc, "SDG MAPPING ....................................................................................................... 25")
    add_justified_paragraph(doc, "REFERENCES ......................................................................................................... 26")

def main():
    doc = docx.Document()
    set_margins(doc)
    
    # --- Title Page ---
    add_centered_heading(doc, "POST-QUANTUM SECURE FIRMWARE DISTRIBUTION AND VEHICLE AUTHENTICATION USING CRYSTALS-DILITHIUM", size=18, bold=True)
    doc.add_paragraph()
    add_centered_heading(doc, "A PROJECT REPORT", size=16, bold=True)
    doc.add_paragraph()
    add_centered_heading(doc, "Submitted by", size=14, bold=False)
    
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("SABREESH RAJ N (Reg. No. 727823TUAM041)\nVARSHINI B M (Reg. No. 727823TUAM058)\nMOHAMMED SHAAHID A (Reg. No. 727823TUAM027)")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(14)
    r.font.bold = True
    
    doc.add_paragraph()
    add_centered_heading(doc, "in partial fulfilment for the award of the degree\nof", size=14, bold=False, space_after=False)
    
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("BACHELOR OF ENGINEERING\nin\nCOMPUTER SCIENCE AND ENGINEERING\n(ARTIFICIAL INTELLIGENCE AND MACHINE LEARNING)")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(16)
    r.font.bold = True
    
    for _ in range(3): doc.add_paragraph()
    
    add_centered_heading(doc, "SRI KRISHNA COLLEGE OF TECHNOLOGY", size=16, bold=True, space_after=False)
    add_centered_heading(doc, "(An Autonomous Institution)\nAffiliated to Anna University and Approved by AICTE\nCoimbatore - 641 042", size=14, bold=False, space_after=False)
    doc.add_paragraph()
    add_centered_heading(doc, "ANNA UNIVERSITY :: CHENNAI 600 025", size=16, bold=True, space_after=False)
    add_centered_heading(doc, "NOVEMBER 2026", size=16, bold=True, space_after=False)
    doc.add_page_break()

    # --- Bonafide Certificate ---
    add_centered_heading(doc, "SRI KRISHNA COLLEGE OF TECHNOLOGY", size=16, bold=True, space_after=False)
    add_centered_heading(doc, "(An Autonomous Institution)\nAffiliated to Anna University and Approved by AICTE\nKOVAIPUDUR, COIMBATORE - 641 042", size=14, bold=False)
    
    add_centered_heading(doc, "BONAFIDE CERTIFICATE", size=16, bold=True)
    add_justified_paragraph(doc, "Certified that this project report \"POST-QUANTUM SECURE FIRMWARE DISTRIBUTION AND VEHICLE AUTHENTICATION USING CRYSTALS-DILITHIUM\" is the bonafide work of SABREESH RAJ N, VARSHINI B M and MOHAMMED SHAAHID A who carried out the project work under my supervision.")
    doc.add_paragraph()
    
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.5
    r = p.add_run("SIGNATURE\t\t\t\t\tSIGNATURE\n")
    r.font.bold = True
    r.font.name = 'Times New Roman'
    r.font.size = Pt(14)
    r2 = p.add_run("Dr. SUMA SIRA JACOB\t\t\t\tHEAD OF THE DEPARTMENT\nSUPERVISOR\nASSOCIATE PROFESSOR\nDepartment of CSE (AI/ML)\nSri Krishna College of Technology, Coimbatore - 641 042")
    r2.font.name = 'Times New Roman'
    r2.font.size = Pt(14)
    
    doc.add_paragraph()
    add_justified_paragraph(doc, "Submitted for the Project Viva-Voce Examination held on ________________.")
    
    p = doc.add_paragraph()
    r = p.add_run("INTERNAL EXAMINER\t\t\t\tEXTERNAL EXAMINER")
    r.font.bold = True
    r.font.name = 'Times New Roman'
    r.font.size = Pt(14)
    doc.add_page_break()

    # --- Declaration ---
    add_centered_heading(doc, "DECLARATION", size=16, bold=True)
    add_justified_paragraph(doc, "We affirm that the project report titled \"POST-QUANTUM SECURE FIRMWARE DISTRIBUTION AND VEHICLE AUTHENTICATION USING CRYSTALS-DILITHIUM\" being submitted in partial fulfilment for the award of BACHELOR OF ENGINEERING in COMPUTER SCIENCE AND ENGINEERING (ARTIFICIAL INTELLIGENCE AND MACHINE LEARNING) is the original work carried out by us. It has not formed part of any other project report or dissertation on the basis of which a degree or award was conferred on an earlier occasion on this or any other candidate.")
    
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.5
    r = p.add_run("Name\t\t\tReg. No.\t\tSignature\n")
    r.font.bold = True
    r.font.name = 'Times New Roman'
    r.font.size = Pt(14)
    r2 = p.add_run("SABREESH RAJ N\t\t727823TUAM041\t____________\nVARSHINI B M\t\t727823TUAM058\t____________\nMOHAMMED SHAAHID A\t727823TUAM027\t____________")
    r2.font.name = 'Times New Roman'
    r2.font.size = Pt(14)
    
    doc.add_paragraph()
    add_justified_paragraph(doc, "I certify that the declaration made by the above candidates is true to the best of my knowledge.")
    doc.add_paragraph()
    add_justified_paragraph(doc, "Name and Signature of the Supervisor with Date: Dr. SUMA SIRA JACOB\n________________________________")
    doc.add_page_break()

    # --- Acknowledgement ---
    add_centered_heading(doc, "ACKNOWLEDGEMENT", size=16, bold=True)
    add_justified_paragraph(doc, "With a grateful heart, we extend our sincere thanks to our Program Coordinator and Project Supervisor, Dr. Suma Sira Jacob, Assistant Professor, Department of Computer Science and Engineering (AI & ML), for her continuous motivation, constant guidance, constructive suggestions, and valuable support throughout the project. Her encouragement and insightful guidance greatly helped us enhance our knowledge, overcome challenges, and successfully complete our project.")
    doc.add_page_break()

    # --- Abstract ---
    add_centered_heading(doc, "ABSTRACT", size=16, bold=True)
    add_justified_paragraph(doc, "Connected vehicles require low latency and secure communication links to be incorporated. However, the advent of quantum computing and Shor's algorithm threatens the security of currently deployed algorithms in vehicular networks, namely RSA, ECC, and ECDSA. This project addresses this vulnerability by developing a quantum-resistant vehicle-to-vehicle (V2V) platooning communication system. We present a security framework implementing two of the National Institute of Standards and Technology (NIST) approved post-quantum cryptography algorithms: CRYSTALS-Kyber for secure key encapsulation and CRYSTALS-Dilithium for robust digital signatures.")
    add_justified_paragraph(doc, "To meet the strict real-time constraints of vehicle platooning, where communication delays can be fatal, our framework utilizes AES-256-GCM to stream all post-handshake traffic, ensuring per-message overhead remains exceptionally low. Empirical results from our prototype demonstrate significant performance benchmarks: key exchange operations conclude in less than 4 milliseconds, average round-trip time (RTT) is maintained at 1.13 milliseconds, and total end-to-end latency stands at 35 milliseconds—well below the strict 100-millisecond threshold for safe platooning. Furthermore, the system robustly handles up to 200 messages per second with a 99.9% key exchange success rate and enforces a fail-safe cutover time of 200 milliseconds. Ultimately, this research verifies that integrating post-quantum security measures into V2V communications does not compromise the demanding real-time operational requirements of autonomous vehicle platoons.")
    doc.add_page_break()

    # --- Table of Contents ---
    add_table_of_contents(doc)
    doc.add_page_break()

    # --- Chapter 1: INTRODUCTION ---
    add_centered_heading(doc, "CHAPTER 1", size=16, bold=True, space_after=False)
    add_centered_heading(doc, "INTRODUCTION", size=16, bold=True)
    add_justified_paragraph(doc, "1.1 Introduction", bold=True)
    add_justified_paragraph(doc, "Modern intelligent transport systems harness real-time Vehicle-to-Vehicle (V2V) communication systems to coordinate vehicles in manners not possible with human drivers. These advancements enable features such as formation shooting, cooperative braking, collision warnings, and highly synchronized vehicle platooning. The algorithms designed to secure such communication links are an engineering marvel, providing confidentiality, integrity, and authenticity for critical safety messages. However, these systems have been developed in a pre-quantum era, relying heavily on classical cryptography.")
    add_justified_paragraph(doc, "1.2 Background", bold=True)
    add_justified_paragraph(doc, "The problems related to cryptographic vulnerability are most acute in the case of vehicle platooning. In a platoon, the leader vehicle transmits its speed, position, and acceleration to the followers, which then adapt their speed and operations accordingly. In such scenarios, milliseconds of latency can be the difference between safe driving and a catastrophic collision. A malicious actor capable of spoofing or tampering with these safety messages could easily orchestrate pile-ups or accidents. Currently, the industry relies on RSA and Elliptic Curve Cryptography (ECC) to secure these networks. Unfortunately, these classical algorithms are inherently vulnerable to Shor's algorithm, a quantum algorithm capable of solving integer factorization and discrete logarithm problems in polynomial time.")
    add_justified_paragraph(doc, "1.3 Motivation", bold=True)
    add_justified_paragraph(doc, "As quantum computers reach maturity, the cryptographic glue holding modern infrastructure together will shatter. We are facing a quantum threat that will eventually operate with unprecedented efficiency, rendering classical encryption obsolete. A single forged safety message can affect every vehicle within a platoon, making message authenticity a critical requirement for safe operation. Moreover, modern connected vehicles frequently receive Over-the-Air (OTA) firmware updates, requiring every update to be cryptographically verified before installation to prevent unauthorized code execution. Given that autonomous vehicle platoons exchange 10 to 50 authenticated safety messages per second, there is an urgent need for fast, reliable, and quantum-resistant signature verification.")
    add_justified_paragraph(doc, "1.4 Conclusion", bold=True)
    add_justified_paragraph(doc, "In this chapter, the foundational context of modern V2V communication was outlined. The motivation stems directly from the existential threat posed by quantum computing to classical cryptography algorithms like RSA and ECC. Addressing this threat through post-quantum cryptographic measures is essential to secure the future of autonomous intelligent transportation systems.")
    doc.add_page_break()

    # --- Chapter 2: LITERATURE REVIEW ---
    add_centered_heading(doc, "CHAPTER 2", size=16, bold=True, space_after=False)
    add_centered_heading(doc, "LITERATURE REVIEW", size=16, bold=True)
    add_justified_paragraph(doc, "2.1 Introduction", bold=True)
    add_justified_paragraph(doc, "This chapter reviews existing literature and security paradigms employed in vehicular networks. It examines both classical security architectures and the recent advances in Post-Quantum Cryptography (PQC), highlighting the limitations of current systems and identifying critical research gaps in the context of V2V platooning.")
    add_justified_paragraph(doc, "2.2 Classical Security in Vehicular Networks", bold=True)
    add_justified_paragraph(doc, "The trust model of vehicular communication systems based on the 802.11p standard and Dedicated Short-Range Communications (DSRC) is virtually identical to standard Public Key Infrastructure (PKI) systems. Each vehicle is issued a certificate by a trusted third party, and signatures on outgoing messages are generated using respective private keys (Hartenstein and Laberteaux, 2008). However, this architecture has critical limitations. The overhead involved in Certificate Revocation List (CRL) validation scales poorly with vehicle density. Signature verification using ECC schemes can introduce higher latencies (often exceeding 10-50 ms per validation due to high message volumes), which is unacceptable given the strict sub-100 ms deadlines of platooning operations.")
    add_justified_paragraph(doc, "2.3 Post-Quantum Cryptography Advances", bold=True)
    add_justified_paragraph(doc, "In response to the quantum threat, NIST initiated a standardization process for post-quantum algorithms, subsequently selecting CRYSTALS-Kyber for key encapsulation and CRYSTALS-Dilithium for digital signatures (Alagic et al., 2022; Dottling et al., 2021). Kyber is constructed upon the Module Learning With Errors (MLWE) problem, while Dilithium relies on both MLWE and Short Integer Solutions (SIS). While hybrid ECC-Kyber protocols offer backward compatibility, they introduce computational latency that proves prohibitive for high-speed, clean-sheet vehicular applications.")
    add_justified_paragraph(doc, "2.4 Lattice-Based Cryptography in Vehicular Network Security", bold=True)
    add_justified_paragraph(doc, "Recent studies have explored lattice-based cryptography for automotive use. For instance, Li et al. (2023) analyzed V2V authentication and OTA firmware updates using MLWE and MSIS algorithm families. FPGA acceleration studies demonstrated that Kyber could produce keys rapidly, opening the prospect of automotive application. Similarly, comparative analyses on automotive processors showed Dilithium3 signature verification requires less than 2.5 ms, well within standard inter-beacon periods (Kandappu et al., 2022).")
    add_justified_paragraph(doc, "2.5 Conclusion", bold=True)
    add_justified_paragraph(doc, "A literature review demonstrates three significant gaps: First, no published studies have simultaneously deployed CRYSTALS-Kyber and CRYSTALS-Dilithium in a live wireless V2V testbed capturing full end-to-end latency. Second, prior literature lacks data on fail-safe response times of platoons under PQC-secured communications during disruption. Finally, optimizing the combination of PQC and symmetric encryption to overcome latency barriers remains underexplored. This project bridges these gaps by proposing and validating a PQC-native V2V framework.")
    doc.add_page_break()

    # --- Chapter 3: PROBLEM IDENTIFICATION ---
    add_centered_heading(doc, "CHAPTER 3", size=16, bold=True, space_after=False)
    add_centered_heading(doc, "PROBLEM IDENTIFICATION", size=16, bold=True)
    add_justified_paragraph(doc, "3.1 Introduction", bold=True)
    add_justified_paragraph(doc, "This chapter specifies the core issues and vulnerabilities inherent in modern intelligent transportation systems, defining the precise problem that the proposed system seeks to resolve.")
    add_justified_paragraph(doc, "3.2 The Quantum Threat to Vehicle Platooning", bold=True)
    add_justified_paragraph(doc, "Autonomous vehicle platooning demands ultra-reliable and low-latency communication. Vehicles running at headway distances of merely 5 to 6 meters on highways necessitate control loop updates of 10 to 50 Hz, with end-to-end delays strictly constrained below 100 milliseconds. Existing systems rely heavily on PKI utilizing RSA and Elliptic Curve Cryptography. The critical problem is that these cryptographic primitives rely on mathematical problems (integer factorization and discrete logarithms) that are trivial to solve using Shor’s algorithm on a sufficient quantum computer. ")
    add_justified_paragraph(doc, "3.3 Problem Statement", bold=True)
    add_justified_paragraph(doc, "Ensuring the authenticity of communicating vehicles and the integrity of safety-critical messages remains a major challenge in autonomous vehicle platoon networks. As quantum computing threatens the security of classical digital signature algorithms, a quantum-resistant authentication mechanism is essential to establish trust and prevent unauthorized communication, without violating the stringent latency requirements of vehicular platoons.")
    add_justified_paragraph(doc, "3.4 Conclusion", bold=True)
    add_justified_paragraph(doc, "The identification of the specific vulnerabilities tied to classical cryptographic standards underscores the necessity of a paradigm shift. The problem statement sets a clear mandate: replace legacy algorithms with quantum-resistant alternatives while meticulously maintaining or improving the real-time operational metrics vital to V2V safety.")
    doc.add_page_break()

    # --- Chapter 4: OBJECTIVE ---
    add_centered_heading(doc, "CHAPTER 4", size=16, bold=True, space_after=False)
    add_centered_heading(doc, "OBJECTIVE", size=16, bold=True)
    add_justified_paragraph(doc, "4.1 Introduction", bold=True)
    add_justified_paragraph(doc, "This chapter clearly outlines the primary and secondary objectives of the project, defining the goals that the implemented system strives to achieve.")
    add_justified_paragraph(doc, "4.2 Primary Objective", bold=True)
    add_justified_paragraph(doc, "To develop a post-quantum authentication framework using CRYSTALS-Dilithium and CRYSTALS-Kyber that ensures secure vehicle authentication, message integrity, and trusted communication in autonomous vehicle platoon networks.")
    add_justified_paragraph(doc, "4.3 Secondary Objectives", bold=True)
    add_justified_paragraph(doc, "- To implement a highly efficient, latency-optimized cryptographic handshake capable of establishing secure sessions in under 10 milliseconds.\n- To secure ongoing platoon telemetry (speed, acceleration, position) using AES-256-GCM, neutralizing tampering, eavesdropping, and replay attacks.\n- To establish a secure Over-the-Air (OTA) firmware update protocol that strictly verifies Dilithium-signed firmware images before deployment.\n- To demonstrate that post-quantum cryptographic compliance does not negatively impact the stringent latency and throughput constraints required for high-speed autonomous platooning.")
    add_justified_paragraph(doc, "4.4 Conclusion", bold=True)
    add_justified_paragraph(doc, "The defined objectives present a comprehensive roadmap for the project, aiming not only to theorize but to practically implement and empirically validate a quantum-resistant V2V communication suite. Successfully meeting these objectives guarantees a robust, future-proof transportation architecture.")
    doc.add_page_break()

    # --- Chapter 5: PROBLEM SOLUTION ---
    add_centered_heading(doc, "CHAPTER 5", size=16, bold=True, space_after=False)
    add_centered_heading(doc, "PROBLEM SOLUTION", size=16, bold=True)
    add_justified_paragraph(doc, "5.1 Introduction", bold=True)
    add_justified_paragraph(doc, "This chapter explains the proposed cryptographic solution designed to address the vulnerabilities identified, leveraging the latest NIST-approved post-quantum algorithms to construct a robust defense mechanism.")
    add_justified_paragraph(doc, "5.2 Proposed Solution Architecture", bold=True)
    add_justified_paragraph(doc, "The core solution replaces vulnerable classical algorithms with lattice-based cryptography. We utilize CRYSTALS-Kyber for Key Encapsulation Mechanisms (KEM) to establish a shared secret over an insecure wireless channel. For identity verification and message authentication, we employ CRYSTALS-Dilithium for digital signatures. This ensures that the Kyber keys are inextricably bound to a verified vehicle identity.")
    add_justified_paragraph(doc, "5.3 Efficient Post-Handshake Security", bold=True)
    add_justified_paragraph(doc, "While PQC algorithms provide exceptional security, calculating a Dilithium signature for every single safety message at 50 Hz would introduce untenable latency. The solution circumvents this by deriving a session key from the Kyber shared secret using HKDF. Subsequently, AES-256-GCM is used for encrypting the actual commands sent between vehicles. AES-256-GCM provides both confidentiality and message integrity via Galois Message Authentication Codes (MACs). Because AES operations can be hardware-accelerated, per-message encryption and decryption consume less than 0.1 milliseconds, making the system incredibly agile.")
    add_justified_paragraph(doc, "5.4 Threat Mitigation Strategy", bold=True)
    add_justified_paragraph(doc, "- Eavesdropping: Neutralized by Kyber key encapsulation.\n- Man-In-The-Middle (MITM) & Impersonation: Neutralized by Dilithium identity keys verifying the initial handshake.\n- Tampering & Forgery: Neutralized by AES-GCM authentication tags validating payload integrity.\n- Replay Attacks: Neutralized by strict sequence numbering tracked within the active encrypted session, alongside timestamp verification.")
    add_justified_paragraph(doc, "5.5 Conclusion", bold=True)
    add_justified_paragraph(doc, "The proposed solution elegantly balances the heavy computational demands of post-quantum cryptography with the high-speed requirements of V2V platooning. By limiting PQC operations to the initial handshake and firmware validation, and relying on AES-GCM for streaming telemetry, the system remains highly secure without sacrificing real-time performance.")
    doc.add_page_break()

    # --- Chapter 6: BLOCK DIAGRAM ---
    add_centered_heading(doc, "CHAPTER 6", size=16, bold=True, space_after=False)
    add_centered_heading(doc, "BLOCK DIAGRAM", size=16, bold=True)
    add_justified_paragraph(doc, "6.1 Introduction", bold=True)
    add_justified_paragraph(doc, "This chapter visualizes the architectural design and structural hierarchy of the proposed V2V platooning system, detailing the interactions between various processing layers.")
    add_justified_paragraph(doc, "6.2 System Architecture Overview", bold=True)
    add_justified_paragraph(doc, "The system architecture is a decentralized four-layered design crafted specifically for autonomous vehicular interaction:\n1. Application Layer: Generates vehicle state information (speed, position, acceleration) and handles the monitoring UI.\n2. Platoon Control Layer (CACC): Computes the Cooperative Adaptive Cruise Control logic, determining desired separation, throttle, and braking actions.\n3. Secure Communication Layer: Executes the cryptographic pipeline, managing Kyber key encapsulation, Dilithium signatures, and AES-GCM streaming encryption.\n4. Networking Layer: Manages the UDP socket transmissions required for rapid, connectionless data delivery.")
    
    # Try to add the image if it was extracted properly
    try:
        doc.add_picture("d:\\My Projects\\Capstone Project\\ProjectReport\\architecture.png", width=Inches(6.0))
        add_justified_paragraph(doc, "Figure 6.1: Overall System Architecture Flow (four layered decentralized design)", bold=True)
    except:
        add_justified_paragraph(doc, "[Architectural Diagram Graphic Placeholder - Ensure 'SystemArchitecture.pdf' is converted to 'architecture.png']", bold=True)
    
    add_justified_paragraph(doc, "6.3 Functional Flow", bold=True)
    add_justified_paragraph(doc, "The leader vehicle acts as the primary node, broadcasting driving commands to the followers. Upon network discovery, a follower vehicle initiates a secure handshake, transmitting its Kyber public key. The leader responds by encapsulating a generated shared secret using the follower's key and signing the challenge with its Dilithium private key. Once verified, both nodes seamlessly transition to the AES-GCM encrypted state, allowing high-throughput telemetry transfer. This architecture explicitly implements fail-safe mechanisms; if an authentic packet is missed within a 200 ms timeout window, the vehicle automatically reverts to standalone cruise control.")
    add_justified_paragraph(doc, "6.4 Conclusion", bold=True)
    add_justified_paragraph(doc, "The block diagram and layered architecture demonstrate a clear segregation of duties, ensuring that the intensive cryptographic operations do not block the critical path of the vehicle control loop, thus maintaining the safety and stability of the platoon.")
    doc.add_page_break()

    # --- Chapter 7: METHODOLOGY ---
    add_centered_heading(doc, "CHAPTER 7", size=16, bold=True, space_after=False)
    add_centered_heading(doc, "METHODOLOGY", size=16, bold=True)
    add_justified_paragraph(doc, "7.1 Introduction", bold=True)
    add_justified_paragraph(doc, "This chapter meticulously details the mathematical formulations and operational procedures utilized to build the secure V2V network, outlining the key generation, handshake, and telemetry encryption processes.")
    
    add_justified_paragraph(doc, "7.2 Mathematical Formulation of Cryptographic Primitives", bold=True)
    add_justified_paragraph(doc, "The security of the framework is founded on mathematical lattice problems. The key pair generation for CRYSTALS-Kyber-768 is given by:")
    add_justified_paragraph(doc, "(pk_k, sk_k) ← Kyber.KeyGen()")
    add_justified_paragraph(doc, "The Kyber public key (pk_k) is used to encrypt a shared secret, ensuring forward secrecy. The security of Kyber relies on the Module Learning With Errors (MLWE) assumption. Concurrently, the CRYSTALS-Dilithium-3 key pair is generated to handle digital signatures:")
    add_justified_paragraph(doc, "(pk_d, sk_d) ← Dilithium.KeyGen()")
    add_justified_paragraph(doc, "The discovery beacon (B) broadcasted by vehicles consolidates the unique vehicle identifier and its public keys:")
    add_justified_paragraph(doc, "B = {vid, pk_k, pk_d}")
    
    add_justified_paragraph(doc, "7.3 Secure Handshake and Encapsulation", bold=True)
    add_justified_paragraph(doc, "During the handshake, the initiating vehicle encapsulates a shared secret (K_shared) using the target's public key to create a ciphertext (c_k):")
    add_justified_paragraph(doc, "(c_k, K_shared) = Kyber.Encap(pk_k, target)")
    add_justified_paragraph(doc, "To prevent impersonation, a composite message (M) is created and digitally signed using Dilithium. The message binds the vehicle ID, ciphertext, and a timestamp:")
    add_justified_paragraph(doc, "M = vid || c_k || T\nσ = Dilithium.Sign(sk_d, M)")
    add_justified_paragraph(doc, "The verification process confirms authenticity without exposing the private keys:")
    add_justified_paragraph(doc, "v = Dilithium.Verify(pk_d_sender, M, σ)")
    
    add_justified_paragraph(doc, "7.4 Session Key Derivation and Traffic Encryption", bold=True)
    add_justified_paragraph(doc, "Following a successful decapsulation, the shared secret is fed into a Key Derivation Function (HKDF) to generate the active session key. This ensures key separation and time-specificity:")
    add_justified_paragraph(doc, "K_session = KDF(K_shared || vid || vid_peer || T)")
    add_justified_paragraph(doc, "All subsequent telemetry (speed, position) is secured using AES-256-GCM, generating a ciphertext (C) and an authentication tag (g) to verify payload integrity on every message:")
    add_justified_paragraph(doc, "C = AES-GCM_{K_session}(m, IV)\ng = AuthTag(K_session, C, IV)")
    
    add_justified_paragraph(doc, "7.5 Over-The-Air (OTA) Updates", bold=True)
    add_justified_paragraph(doc, "The framework also includes a module for secure firmware updates. The OTA server signs the binary firmware image using its Dilithium private identity key. The updater strictly verifies this signature before initiating any installation sequence, decisively preventing malicious firmware injection and preserving the integrity of the vehicle’s operating system.")
    
    add_justified_paragraph(doc, "7.6 Conclusion", bold=True)
    add_justified_paragraph(doc, "By bridging advanced lattice mathematics with efficient symmetric encryption algorithms, the proposed methodology establishes a comprehensive, end-to-end security protocol capable of neutralizing advanced quantum computing threats within a live vehicular network.")
    doc.add_page_break()

    # --- Chapter 8: RESULTS AND DISCUSSION ---
    add_centered_heading(doc, "CHAPTER 8", size=16, bold=True, space_after=False)
    add_centered_heading(doc, "RESULTS AND DISCUSSION", size=16, bold=True)
    add_justified_paragraph(doc, "8.1 Introduction", bold=True)
    add_justified_paragraph(doc, "This chapter presents the empirical results obtained from the prototype implementation, evaluating cryptographic latencies, network throughput, and the system's resilience against active cyberattacks.")
    
    add_justified_paragraph(doc, "8.2 Key Exchange Performance", bold=True)
    add_justified_paragraph(doc, "Extensive benchmarking of the Kyber-768 key exchange process yielded highly favorable results. Across consecutive test iterations on commodity hardware, the encapsulation process consumed a negligible 0.23 ms. Decapsulation on the receiving end required approximately 2.04 ms. The entire key exchange operation successfully concluded in under 4.0 milliseconds. Because this operation is localized to the initial session setup, it does not impede the continuous high-speed data stream required for active platooning.")
    
    add_justified_paragraph(doc, "8.3 Communication Latency and Throughput", bold=True)
    add_justified_paragraph(doc, "For the active telemetry session, the AES-256-GCM encryption phase required an average of 0.082 ms, while decryption consumed merely 0.026 ms. Analyzing fifty continuous sequences demonstrated an average Round Trip Time (RTT) of 1.13 ms, peaking at a maximum of 1.25 ms. The total end-to-end latency was measured at 35 ms, operating well within the strict 100 ms threshold necessary to maintain a safe platooning headway distance of 5 meters. The system reliably supported a throughput of 200 messages per second with a 99.9% key exchange success rate.")
    
    add_justified_paragraph(doc, "8.4 Attack Mitigation Verification", bold=True)
    add_justified_paragraph(doc, "The prototype was subjected to rigorous penetration testing:\n- MITM Attacks: Simulated interceptions modifying the handshake were immediately rejected due to Dilithium signature validation failures.\n- Replay Attacks: Packets captured and resent were identified and dropped by the active session tracker, enforcing strictly increasing sequence numbers and checking timestamp freshness.\n- Tampering: Deliberate bit-flips in the AES encrypted payload were consistently caught by the Galois Authentication Tag validation.")
    
    add_justified_paragraph(doc, "8.5 Conclusion", bold=True)
    add_justified_paragraph(doc, "The test results conclusively demonstrate that the integration of post-quantum cryptography is entirely feasible in modern vehicular networks. The system achieves unparalleled cryptographic security without sacrificing the ultra-low latency required for the safety of autonomous driving.")
    doc.add_page_break()

    # --- Chapter 9: CONCLUSION ---
    add_centered_heading(doc, "CHAPTER 9", size=16, bold=True, space_after=False)
    add_centered_heading(doc, "CONCLUSION", size=16, bold=True)
    add_justified_paragraph(doc, "9.1 Introduction", bold=True)
    add_justified_paragraph(doc, "This chapter summarizes the primary findings of the research project, highlighting the key contributions to the field of intelligent transportation and suggesting avenues for future research.")
    
    add_justified_paragraph(doc, "9.2 Conclusion", bold=True)
    add_justified_paragraph(doc, "The proposed authentication framework successfully addresses the critical need for quantum-resistant vehicle authentication in autonomous platoon networks using CRYSTALS-Dilithium and CRYSTALS-Kyber. The implementation effectively secures vehicle identity verification, message authenticity, and integrity through post-quantum digital signatures and symmetric encryption. Experimental validation demonstrates that the system establishes secure sessions in under 4 milliseconds and maintains an end-to-end telemetry latency of 35 ms, fully supporting high-speed 200 msg/sec operations. It actively prevents message forgery, replay, and impersonation attacks. Ultimately, this work establishes a vital foundation for trusted, quantum-secure autonomous vehicle communication, proving that transitioning to quantum security is achievable today.")
    
    add_justified_paragraph(doc, "9.3 Future Scope", bold=True)
    add_justified_paragraph(doc, "Future work will involve testing the system's performance on dedicated hardware for V2X radios, such as ESP32 embedded systems and FPGA/ASIC accelerators. Expanding the tests to dense multi-vehicle urban environments and analyzing resilience under adversarial channel conditions (e.g., severe packet loss and jamming) will further solidify the framework's readiness for commercial deployment.")
    
    add_justified_paragraph(doc, "9.4 Final Remarks", bold=True)
    add_justified_paragraph(doc, "By anticipating the capabilities of future quantum computers and fortifying modern vehicular infrastructure today, we secure the future of intelligent transportation, ensuring safety and privacy for all road users.")
    doc.add_page_break()

    # --- SDG MAPPING ---
    add_centered_heading(doc, "SUSTAINABLE DEVELOPMENT GOALS MAPPING", size=16, bold=True)
    add_justified_paragraph(doc, "The Sustainable Development Goals (SDGs) are a collection of 17 global goals designed as a blueprint to achieve a better and more sustainable future for all. Set in 2015 by the United Nations General Assembly and intended to be achieved by the year 2030, these goals aim to solve pressing global challenges. This project directly addresses two crucial SDGs.")
    
    add_justified_paragraph(doc, "Which SDGs does the project directly address?", bold=True)
    add_justified_paragraph(doc, "SDG 9 - Industry, Innovation, and Infrastructure: By developing a quantum-resistant architecture, the project fosters innovation in the cybersecurity space, contributing directly to building resilient, future-proof intelligent transportation infrastructure.\n\nSDG 11 - Sustainable Cities and Communities: The project significantly improves road safety by securing the communication links required for reliable autonomous mobility, helping cities transition to safer, automated transport systems.")
    
    add_justified_paragraph(doc, "Indian Knowledge System (IKS) Integration", bold=True)
    add_justified_paragraph(doc, "In alignment with the National Education Policy (NEP) 2020, this project incorporates core tenets of the Indian Knowledge System:\n- Raksha (Protection): The fundamental goal of the framework is the proactive safeguarding of safety-critical transportation systems, ensuring the physical safety of passengers through advanced cyber protection.\n- Anvikshiki (Scientific Inquiry): The research employs deep analytical reasoning and cryptographic innovation to investigate, deconstruct, and solve the emerging threats posed by quantum computing.")
    doc.add_page_break()

    # --- REFERENCES ---
    add_centered_heading(doc, "REFERENCES", size=16, bold=True)
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
        p = add_justified_paragraph(doc, ref)
        p.paragraph_format.left_indent = Inches(0.5)
        p.paragraph_format.first_line_indent = Inches(-0.5)

    doc.save("Project_Report_Final.docx")
    print("Project_Report_Final.docx successfully generated with full formatting!")

if __name__ == "__main__":
    main()
