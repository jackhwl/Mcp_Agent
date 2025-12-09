ai_ticket_spec:
  version: 1.0
  type: <story|bug|task>            # REQUIRED
  summary: ""                       # REQUIRED, non-empty, not "."
  epic_link: ""                     # REQUIRED, must reference an Epic not in Closed
  tech_category: ""                 # REQUIRED, must match Epic's Tech Category
  attachments: []                   # Optional: URLs (Figma, logs, videos, specs)

  story:                            # Present only when type=story
    as_a: ""                        # REQUIRED, e.g., "Consumer", "Dev", "Product Manager"; not "."
    i_want_to: ""                   # REQUIRED; not "."
    so_that: ""                     # REQUIRED; not "."
    description: ""                 # REQUIRED; background, scope
    acceptance_criteria:            # REQUIRED; Gherkin/bullets; must define "done"
      - "Given ..., When ..., Then ..."
    user_impact: ""                 # Optional; who/how often/risk
    dependencies: []                # Optional; tickets/APIs/systems
    assumptions: []                 # Optional

  bug:                              # Present only when type=bug
    description: ""                 # REQUIRED; when it started + impact
    steps_to_reproduce:             # REQUIRED; numbered atomic steps
      - "1) ..."
      - "2) ..."
    expected_result: ""             # REQUIRED
    actual_result: ""               # REQUIRED
    detected_in:                    # REQUIRED; env details
      browser: ""
      os: ""
      device: ""
      environment: ""               # Staging/Prod/etc.
    detected_by: ""                 # REQUIRED; Automated/Manual/Internal/External
    severity: "<Critical|High|Medium|Low>"  # REQUIRED
    priority: "<Critical|High|Medium|Low|Minor|Unprioritized>"  # REQUIRED
    sprint: ""                      # Optional
    logs_screenshots: []            # REQUIRED to attach when available

  task:                             # Present only when type=task
    description: ""                 # REQUIRED; objective + steps + tools
    acceptance_criteria:            # REQUIRED if validation is needed
      - "Given ..., When ..., Then ..."
    dependencies: []                # Optional
