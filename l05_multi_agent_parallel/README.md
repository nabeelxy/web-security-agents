# Parallel Agent

This toy example shows how parallel agents pattern works.

It parallelly fetches information about a domain (whois_agent and cert_agent) and then uses a report_agent to synthesize the findings.

## Architecture
Sequential(Parallel(whois_agent, cert_agent) -> report_agent)
