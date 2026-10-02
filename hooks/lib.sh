# Sourced by the hooks. Prints the value of a status.md field ($2) from file $1.
# Accepts "- **next:** x", "- **next**: x" and plain "next: x".
field() {
  sed -nE "s/^[-*[:space:]]*(\*\*)?$2(\*\*)?:?(\*\*)?:?[[:space:]]*//p" "$1" | head -n1 |
    sed -E 's/[[:space:]]+$//'
}
# True when a value is empty, "none", or an unfilled <...> template placeholder.
is_empty() {
  case "$(printf '%s' "$1" | tr '[:upper:]' '[:lower:]')" in
    ""|none|"none."|"<"*">") return 0 ;;
  esac
  return 1
}
