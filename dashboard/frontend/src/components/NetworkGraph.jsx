import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Shield, ShieldAlert, Cpu } from 'lucide-react';

const NetworkGraph = ({ events }) => {
  const [mitmActive, setMitmActive] = useState(false);
  const [packets, setPackets] = useState([]);

  useEffect(() => {
    if (events.length === 0) {
      setMitmActive(false);
      setPackets([]);
      return;
    }

    const latest = events[events.length - 1];
    const msg = latest.message || "";

    if (msg.includes("attacker") || msg.includes("MITM")) {
      setMitmActive(true);
    }

    // Trigger packet animation based on log events
    if (msg.includes("sent") || msg.includes("encapsulated") || msg.includes("ACK") || msg.includes("STOLEN")) {
      const isAttackerInvolved = mitmActive && !msg.includes("ACK"); // rough heuristic
      const fromNode = isAttackerInvolved && msg.includes("STOLEN") ? "mitm" : "leader";
      const toNode = msg.includes("ACK") ? "leader" : isAttackerInvolved ? "mitm" : "follower";
      
      const newPacket = {
        id: Date.now(),
        from: fromNode,
        to: toNode,
        color: msg.includes("BRAKE") || msg.includes("STOLEN") ? "#ef4444" : "#3b82f6"
      };
      
      setPackets(p => [...p, newPacket]);
      
      // Remove packet after animation
      setTimeout(() => {
        setPackets(p => p.filter(pkt => pkt.id !== newPacket.id));
      }, 1000);
    }
  }, [events]);

  const getNodePos = (id) => {
    switch(id) {
      case 'leader': return { left: '15%', top: '50%' };
      case 'follower': return { left: '85%', top: '50%' };
      case 'mitm': return { left: '50%', top: '50%' };
      default: return { left: '50%', top: '50%' };
    }
  };

  return (
    <div className="w-full h-full relative bg-gray-900 flex items-center justify-center p-8">
      {/* Background connection lines */}
      <svg className="absolute inset-0 w-full h-full" style={{ zIndex: 0 }}>
        <line x1="15%" y1="50%" x2="85%" y2="50%" stroke="rgba(255,255,255,0.1)" strokeWidth="2" strokeDasharray="5,5" />
      </svg>

      {/* Nodes */}
      <div className="absolute" style={{ left: '15%', top: '50%', transform: 'translate(-50%, -50%)', zIndex: 10 }}>
        <div className="glass p-4 rounded-full neon-border-blue flex flex-col items-center gap-2">
          <Cpu className="w-8 h-8 text-blue-400" />
          <span className="font-bold text-sm">Leader</span>
        </div>
      </div>

      <AnimatePresence>
        {mitmActive && (
          <motion.div 
            initial={{ scale: 0, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            className="absolute" style={{ left: '50%', top: '50%', transform: 'translate(-50%, -50%)', zIndex: 10 }}
          >
            <div className="glass p-4 rounded-full neon-border-red flex flex-col items-center gap-2 bg-red-900 bg-opacity-20">
              <ShieldAlert className="w-8 h-8 text-red-500 animate-pulse" />
              <span className="font-bold text-sm text-red-400">Attacker (MITM)</span>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      <div className="absolute" style={{ left: '85%', top: '50%', transform: 'translate(-50%, -50%)', zIndex: 10 }}>
        <div className="glass p-4 rounded-full neon-border-green flex flex-col items-center gap-2">
          <Shield className="w-8 h-8 text-green-400" />
          <span className="font-bold text-sm">Follower</span>
        </div>
      </div>

      {/* Animated Packets */}
      {packets.map(pkt => {
        const from = getNodePos(pkt.from);
        const to = getNodePos(pkt.to);
        return (
          <motion.div
            key={pkt.id}
            initial={{ left: from.left, top: from.top, opacity: 1, scale: 1 }}
            animate={{ left: to.left, top: to.top, opacity: 0.5, scale: 0.5 }}
            transition={{ duration: 0.8, ease: "easeInOut" }}
            className="absolute w-4 h-4 rounded-full"
            style={{ 
              backgroundColor: pkt.color, 
              transform: 'translate(-50%, -50%)',
              boxShadow: `0 0 15px ${pkt.color}`,
              zIndex: 5
            }}
          />
        );
      })}
    </div>
  );
};

// Need AnimatePresence here too
import { AnimatePresence } from 'framer-motion';

export default NetworkGraph;
