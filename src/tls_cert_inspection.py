import ssl

def tls_cert_inspection(domain: str):
    try:
        ctx = ssl.create_default_context()
        with ctx.wrap_socket(
            socket.socket(),
            server_hostname=domain
        ) as s:
            s.settimeout(5)
            s.connect((domain, 443))
            cert = s.getpeercert()
        return {
            "issuer": dict(cert.get("issuer", [])),
            "subject": dict(cert.get("subject", [])),
            "not_before": cert.get("notBefore", ""),
            "not_after": cert.get("notAfter", "")
        }
        
    except Exception as e:
        print(f"Error inspecting TLS certificate: {e}")
        return None