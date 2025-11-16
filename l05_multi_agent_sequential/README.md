# Sequential Workflow

This toy example shows how to build a sequential agents workflow for identifying the ASN of a given domain.

In order to identify the ASN, first the NS lookup agent is invoked to identify the hosting IPs and then ASN agent is used to get the ASN for these IPs.

## Architecture

Sequential(ns_lookup_agent -> asn_agent)
