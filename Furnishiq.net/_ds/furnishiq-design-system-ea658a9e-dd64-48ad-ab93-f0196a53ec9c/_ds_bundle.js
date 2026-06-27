/* @ds-bundle: {"format":3,"namespace":"FurnishIQDesignSystem_ea658a","components":[{"name":"Badge","sourcePath":"components/core/Badge.jsx"},{"name":"Button","sourcePath":"components/core/Button.jsx"},{"name":"Card","sourcePath":"components/core/Card.jsx"},{"name":"Divider","sourcePath":"components/core/Divider.jsx"},{"name":"Input","sourcePath":"components/forms/Input.jsx"},{"name":"Select","sourcePath":"components/forms/Select.jsx"},{"name":"Textarea","sourcePath":"components/forms/Textarea.jsx"},{"name":"Nav","sourcePath":"components/navigation/Nav.jsx"}],"sourceHashes":{"components/core/Badge.jsx":"e6eb94161187","components/core/Button.jsx":"4bafee7e71eb","components/core/Card.jsx":"b72206754c30","components/core/Divider.jsx":"6da2b4190471","components/forms/Input.jsx":"acb2dbc6bf19","components/forms/Select.jsx":"917a444aaa37","components/forms/Textarea.jsx":"6093a0584d24","components/navigation/Nav.jsx":"694b635e8739"},"inlinedExternals":[],"unexposedExports":[]} */

(() => {

const __ds_ns = (window.FurnishIQDesignSystem_ea658a = window.FurnishIQDesignSystem_ea658a || {});

const __ds_scope = {};

(__ds_ns.__errors = __ds_ns.__errors || []);

// components/core/Badge.jsx
try { (() => {
/**
 * FurnishIQ Badge — compact status labels and category tags.
 */
function Badge({
  children,
  variant = 'default',
  size = 'md'
}) {
  const variants = {
    /* ── Walnut palette ── */
    default: {
      background: 'var(--color-stone)',
      color: 'var(--color-walnut)',
      border: '1px solid var(--color-champagne)'
    },
    primary: {
      background: 'var(--color-walnut)',
      color: 'var(--color-white)',
      border: 'none'
    },
    bronze: {
      background: 'var(--color-bronze)',
      color: 'var(--color-white)',
      border: 'none'
    },
    outline: {
      background: 'transparent',
      color: 'var(--color-walnut)',
      border: '1px solid var(--color-walnut)'
    },
    dark: {
      background: 'var(--color-charcoal)',
      color: 'var(--color-white)',
      border: 'none'
    },
    champagne: {
      background: 'var(--color-champagne)',
      color: 'var(--color-walnut-dark)',
      border: 'none'
    },
    taupe: {
      background: 'transparent',
      color: 'var(--color-taupe)',
      border: '1px solid var(--color-taupe)'
    },
    /* ── Green palette ── */
    green: {
      background: 'var(--color-brand-green)',
      color: '#FFFFFF',
      border: 'none'
    },
    'green-dark': {
      background: 'var(--color-green-dark)',
      color: '#FFFFFF',
      border: 'none'
    },
    'green-light': {
      background: 'var(--color-green-stone)',
      color: 'var(--color-green-dark)',
      border: '1px solid var(--color-green-pale)'
    },
    'green-outline': {
      background: 'transparent',
      color: 'var(--color-brand-green)',
      border: '1px solid var(--color-brand-green)'
    },
    'green-sage': {
      background: 'var(--color-green-mist)',
      color: 'var(--color-green-dark)',
      border: '1px solid var(--color-green-sage)'
    }
  };
  const sizes = {
    sm: {
      padding: '3px 10px',
      fontSize: '8px'
    },
    md: {
      padding: '4px 12px',
      fontSize: '9px'
    },
    lg: {
      padding: '6px 16px',
      fontSize: '10px'
    }
  };
  return /*#__PURE__*/React.createElement("span", {
    style: {
      display: 'inline-block',
      ...sizes[size],
      ...variants[variant],
      fontFamily: 'var(--font-body)',
      fontWeight: 'var(--weight-semibold)',
      letterSpacing: 'var(--tracking-widest)',
      textTransform: 'uppercase',
      whiteSpace: 'nowrap',
      borderRadius: 'var(--radius-none)'
    }
  }, children);
}
Object.assign(__ds_scope, { Badge });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/Badge.jsx", error: String((e && e.message) || e) }); }

// components/core/Button.jsx
try { (() => {
/**
 * FurnishIQ Button — luxury CTA component.
 * Uses sharp corners (no border-radius) per brand guidelines.
 * All text is uppercase with wide letter-spacing.
 */
function Button({
  children,
  variant = 'primary',
  size = 'md',
  disabled = false,
  onClick,
  fullWidth = false,
  type = 'button',
  href
}) {
  const base = {
    display: 'inline-flex',
    alignItems: 'center',
    justifyContent: 'center',
    gap: '8px',
    fontFamily: 'var(--font-body)',
    fontWeight: 'var(--weight-semibold)',
    letterSpacing: 'var(--tracking-widest)',
    textTransform: 'uppercase',
    cursor: disabled ? 'not-allowed' : 'pointer',
    opacity: disabled ? 0.45 : 1,
    border: 'none',
    borderRadius: 'var(--radius-none)',
    transition: 'background var(--transition-base), color var(--transition-base), border-color var(--transition-base)',
    textDecoration: 'none',
    width: fullWidth ? '100%' : 'auto',
    whiteSpace: 'nowrap'
  };
  const sizes = {
    sm: {
      padding: '10px 24px',
      fontSize: '10px'
    },
    md: {
      padding: '14px 36px',
      fontSize: '11px'
    },
    lg: {
      padding: '18px 52px',
      fontSize: '12px'
    },
    xl: {
      padding: '22px 64px',
      fontSize: '13px'
    }
  };
  const variants = {
    /* ── Walnut palette ── */
    primary: {
      background: 'var(--color-walnut)',
      color: 'var(--color-white)',
      border: 'none'
    },
    secondary: {
      background: 'transparent',
      color: 'var(--color-walnut)',
      border: '1.5px solid var(--color-walnut)'
    },
    ghost: {
      background: 'transparent',
      color: 'var(--color-walnut)',
      border: '1.5px solid transparent',
      textDecoration: 'underline',
      textUnderlineOffset: '4px'
    },
    dark: {
      background: 'var(--color-charcoal)',
      color: 'var(--color-white)',
      border: 'none'
    },
    bronze: {
      background: 'var(--color-bronze)',
      color: 'var(--color-white)',
      border: 'none'
    },
    light: {
      background: 'var(--color-white)',
      color: 'var(--color-walnut)',
      border: 'none'
    },
    /* ── Green palette ── */
    green: {
      background: 'var(--color-brand-green)',
      color: 'var(--color-white)',
      border: 'none'
    },
    'green-dark': {
      background: 'var(--color-green-dark)',
      color: 'var(--color-white)',
      border: 'none'
    },
    'green-outline': {
      background: 'transparent',
      color: 'var(--color-brand-green)',
      border: '1.5px solid var(--color-brand-green)'
    },
    'green-ghost': {
      background: 'transparent',
      color: 'var(--color-brand-green)',
      border: '1.5px solid transparent',
      textDecoration: 'underline',
      textUnderlineOffset: '4px'
    },
    'green-light': {
      background: 'var(--color-green-stone)',
      color: 'var(--color-green-dark)',
      border: 'none'
    }
  };
  const style = {
    ...base,
    ...sizes[size],
    ...variants[variant]
  };
  if (href) {
    return /*#__PURE__*/React.createElement("a", {
      href: href,
      style: style
    }, children);
  }
  return /*#__PURE__*/React.createElement("button", {
    type: type,
    style: style,
    disabled: disabled,
    onClick: onClick
  }, children);
}
Object.assign(__ds_scope, { Button });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/Button.jsx", error: String((e && e.message) || e) }); }

// components/core/Card.jsx
try { (() => {
/**
 * FurnishIQ Card — container component for project tiles,
 * service listings, testimonials, and content blocks.
 */
function Card({
  children,
  variant = 'default',
  radius = 'none',
  padding = 'md',
  border = true,
  shadow = false,
  onClick,
  style: customStyle,
  as: Tag = 'div'
}) {
  const paddings = {
    none: '0',
    sm: '16px 20px',
    md: '28px 32px',
    lg: '40px 48px',
    xl: '56px 64px'
  };
  const variants = {
    default: {
      background: 'var(--color-white)',
      borderColor: 'var(--color-champagne)'
    },
    stone: {
      background: 'var(--color-stone)',
      borderColor: 'var(--color-champagne)'
    },
    dark: {
      background: 'var(--color-charcoal)',
      borderColor: 'rgba(214,194,168,0.2)'
    },
    walnut: {
      background: 'var(--color-walnut-dark)',
      borderColor: 'rgba(139,107,74,0.3)'
    },
    champagne: {
      background: 'var(--color-champagne)',
      borderColor: 'var(--color-taupe)'
    },
    /* ── Green palette ── */
    'green-dark': {
      background: 'var(--color-green-dark)',
      borderColor: 'rgba(90,184,114,0.2)'
    },
    'green-forest': {
      background: 'var(--color-green-forest)',
      borderColor: 'rgba(142,212,160,0.25)'
    },
    'green-stone': {
      background: 'var(--color-green-stone)',
      borderColor: 'var(--color-green-pale)'
    },
    'green-mist': {
      background: 'var(--color-green-mist)',
      borderColor: 'var(--color-green-sage)'
    }
  };
  const radii = {
    none: '0',
    sm: 'var(--radius-sm)',
    md: 'var(--radius-md)',
    lg: 'var(--radius-lg)'
  };
  const style = {
    padding: paddings[padding],
    border: border ? `1px solid ${variants[variant].borderColor}` : 'none',
    background: variants[variant].background,
    borderRadius: radii[radius],
    boxShadow: shadow ? 'var(--shadow-md)' : 'none',
    cursor: onClick ? 'pointer' : 'default',
    transition: shadow ? 'box-shadow var(--transition-base)' : 'none',
    position: 'relative',
    ...customStyle
  };
  return /*#__PURE__*/React.createElement(Tag, {
    style: style,
    onClick: onClick
  }, children);
}
Object.assign(__ds_scope, { Card });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/Card.jsx", error: String((e && e.message) || e) }); }

// components/core/Divider.jsx
try { (() => {
/**
 * FurnishIQ Divider — decorative section separator.
 * Used between content sections to maintain editorial rhythm.
 */
function Divider({
  variant = 'line',
  label,
  color = 'champagne'
}) {
  const colors = {
    champagne: 'var(--color-champagne)',
    walnut: 'var(--color-walnut)',
    bronze: 'var(--color-bronze)',
    taupe: 'var(--color-taupe)',
    green: 'var(--color-brand-green)',
    'green-sage': 'var(--color-green-sage)',
    'green-pale': 'var(--color-green-pale)'
  };
  if (variant === 'ornamental') {
    return /*#__PURE__*/React.createElement("div", {
      style: {
        display: 'flex',
        alignItems: 'center',
        gap: '16px',
        padding: '8px 0'
      }
    }, /*#__PURE__*/React.createElement("div", {
      style: {
        flex: 1,
        height: '1px',
        background: colors[color]
      }
    }), /*#__PURE__*/React.createElement("div", {
      style: {
        width: '6px',
        height: '6px',
        background: colors[color],
        transform: 'rotate(45deg)',
        flexShrink: 0
      }
    }), /*#__PURE__*/React.createElement("div", {
      style: {
        flex: 1,
        height: '1px',
        background: colors[color]
      }
    }));
  }
  if (variant === 'labeled') {
    return /*#__PURE__*/React.createElement("div", {
      style: {
        display: 'flex',
        alignItems: 'center',
        gap: '20px',
        padding: '8px 0'
      }
    }, /*#__PURE__*/React.createElement("div", {
      style: {
        flex: 1,
        height: '1px',
        background: colors[color]
      }
    }), /*#__PURE__*/React.createElement("span", {
      style: {
        fontFamily: 'var(--font-body)',
        fontSize: '9px',
        fontWeight: 'var(--weight-semibold)',
        letterSpacing: 'var(--tracking-widest)',
        textTransform: 'uppercase',
        color: colors[color],
        whiteSpace: 'nowrap'
      }
    }, label), /*#__PURE__*/React.createElement("div", {
      style: {
        flex: 1,
        height: '1px',
        background: colors[color]
      }
    }));
  }
  return /*#__PURE__*/React.createElement("div", {
    style: {
      height: '1px',
      background: colors[color],
      width: '100%'
    }
  });
}
Object.assign(__ds_scope, { Divider });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/Divider.jsx", error: String((e && e.message) || e) }); }

// components/forms/Input.jsx
try { (() => {
/**
 * FurnishIQ Input — single-line text input with label, hint, and error states.
 */
function Input({
  label,
  placeholder,
  value,
  onChange,
  type = 'text',
  required = false,
  disabled = false,
  error,
  hint,
  name,
  size = 'md'
}) {
  const sizes = {
    sm: {
      padding: '10px 14px',
      fontSize: '13px',
      height: '40px'
    },
    md: {
      padding: '14px 16px',
      fontSize: '14px',
      height: '50px'
    },
    lg: {
      padding: '18px 20px',
      fontSize: '16px',
      height: '60px'
    }
  };
  return /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      flexDirection: 'column',
      gap: '6px'
    }
  }, label && /*#__PURE__*/React.createElement("label", {
    style: {
      fontFamily: 'var(--font-body)',
      fontSize: '10px',
      fontWeight: 'var(--weight-semibold)',
      letterSpacing: 'var(--tracking-widest)',
      textTransform: 'uppercase',
      color: error ? '#9B2C2C' : 'var(--color-walnut)'
    }
  }, label, required && /*#__PURE__*/React.createElement("span", {
    style: {
      color: 'var(--color-bronze)',
      marginLeft: '4px'
    }
  }, "*")), /*#__PURE__*/React.createElement("input", {
    type: type,
    name: name,
    value: value,
    onChange: onChange,
    placeholder: placeholder,
    disabled: disabled,
    style: {
      ...sizes[size],
      fontFamily: 'var(--font-body)',
      border: error ? '1.5px solid #9B2C2C' : '1px solid var(--color-champagne)',
      borderRadius: 'var(--radius-none)',
      background: disabled ? 'var(--color-stone)' : 'var(--color-white)',
      color: 'var(--color-charcoal)',
      outline: 'none',
      transition: 'border-color var(--transition-fast)',
      width: '100%',
      boxSizing: 'border-box',
      opacity: disabled ? 0.6 : 1
    },
    onFocus: e => {
      if (!error) e.target.style.borderColor = 'var(--color-walnut)';
    },
    onBlur: e => {
      if (!error) e.target.style.borderColor = 'var(--color-champagne)';
    }
  }), error && /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: 'var(--font-body)',
      fontSize: '11px',
      color: '#9B2C2C',
      letterSpacing: '0.03em'
    }
  }, error), hint && !error && /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: 'var(--font-body)',
      fontSize: '11px',
      color: 'var(--color-bronze)',
      letterSpacing: '0.03em'
    }
  }, hint));
}
Object.assign(__ds_scope, { Input });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/forms/Input.jsx", error: String((e && e.message) || e) }); }

// components/forms/Select.jsx
try { (() => {
/**
 * FurnishIQ Select — dropdown field matching Input visual style.
 */
function Select({
  label,
  options = [],
  value,
  onChange,
  placeholder,
  disabled = false,
  error,
  hint,
  required = false,
  name,
  size = 'md'
}) {
  const sizes = {
    sm: {
      padding: '10px 14px',
      fontSize: '13px',
      height: '40px'
    },
    md: {
      padding: '14px 16px',
      fontSize: '14px',
      height: '50px'
    },
    lg: {
      padding: '18px 20px',
      fontSize: '16px',
      height: '60px'
    }
  };
  return /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      flexDirection: 'column',
      gap: '6px'
    }
  }, label && /*#__PURE__*/React.createElement("label", {
    style: {
      fontFamily: 'var(--font-body)',
      fontSize: '10px',
      fontWeight: 'var(--weight-semibold)',
      letterSpacing: 'var(--tracking-widest)',
      textTransform: 'uppercase',
      color: error ? '#9B2C2C' : 'var(--color-walnut)'
    }
  }, label, required && /*#__PURE__*/React.createElement("span", {
    style: {
      color: 'var(--color-bronze)',
      marginLeft: '4px'
    }
  }, "*")), /*#__PURE__*/React.createElement("div", {
    style: {
      position: 'relative'
    }
  }, /*#__PURE__*/React.createElement("select", {
    name: name,
    value: value,
    onChange: onChange,
    disabled: disabled,
    style: {
      ...sizes[size],
      paddingRight: '40px',
      fontFamily: 'var(--font-body)',
      border: error ? '1.5px solid #9B2C2C' : '1px solid var(--color-champagne)',
      borderRadius: 'var(--radius-none)',
      background: disabled ? 'var(--color-stone)' : 'var(--color-white)',
      color: value ? 'var(--color-charcoal)' : 'var(--color-taupe)',
      outline: 'none',
      width: '100%',
      boxSizing: 'border-box',
      appearance: 'none',
      cursor: disabled ? 'not-allowed' : 'pointer',
      opacity: disabled ? 0.6 : 1
    }
  }, placeholder && /*#__PURE__*/React.createElement("option", {
    value: ""
  }, placeholder), options.map(opt => /*#__PURE__*/React.createElement("option", {
    key: opt.value,
    value: opt.value
  }, opt.label))), /*#__PURE__*/React.createElement("div", {
    style: {
      position: 'absolute',
      right: '14px',
      top: '50%',
      transform: 'translateY(-50%)',
      pointerEvents: 'none',
      color: 'var(--color-bronze)'
    }
  }, /*#__PURE__*/React.createElement("svg", {
    width: "12",
    height: "8",
    viewBox: "0 0 12 8",
    fill: "none"
  }, /*#__PURE__*/React.createElement("path", {
    d: "M1 1L6 7L11 1",
    stroke: "currentColor",
    strokeWidth: "1.5",
    strokeLinecap: "square"
  })))), error && /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: 'var(--font-body)',
      fontSize: '11px',
      color: '#9B2C2C'
    }
  }, error), hint && !error && /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: 'var(--font-body)',
      fontSize: '11px',
      color: 'var(--color-bronze)'
    }
  }, hint));
}
Object.assign(__ds_scope, { Select });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/forms/Select.jsx", error: String((e && e.message) || e) }); }

// components/forms/Textarea.jsx
try { (() => {
/**
 * FurnishIQ Textarea — multi-line text input.
 */
function Textarea({
  label,
  placeholder,
  value,
  onChange,
  required = false,
  disabled = false,
  error,
  hint,
  name,
  rows = 4
}) {
  return /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      flexDirection: 'column',
      gap: '6px'
    }
  }, label && /*#__PURE__*/React.createElement("label", {
    style: {
      fontFamily: 'var(--font-body)',
      fontSize: '10px',
      fontWeight: 'var(--weight-semibold)',
      letterSpacing: 'var(--tracking-widest)',
      textTransform: 'uppercase',
      color: error ? '#9B2C2C' : 'var(--color-walnut)'
    }
  }, label, required && /*#__PURE__*/React.createElement("span", {
    style: {
      color: 'var(--color-bronze)',
      marginLeft: '4px'
    }
  }, "*")), /*#__PURE__*/React.createElement("textarea", {
    name: name,
    value: value,
    onChange: onChange,
    placeholder: placeholder,
    disabled: disabled,
    rows: rows,
    style: {
      padding: '14px 16px',
      fontFamily: 'var(--font-body)',
      fontSize: '14px',
      lineHeight: '1.6',
      border: error ? '1.5px solid #9B2C2C' : '1px solid var(--color-champagne)',
      borderRadius: 'var(--radius-none)',
      background: disabled ? 'var(--color-stone)' : 'var(--color-white)',
      color: 'var(--color-charcoal)',
      outline: 'none',
      width: '100%',
      boxSizing: 'border-box',
      resize: 'vertical',
      opacity: disabled ? 0.6 : 1
    },
    onFocus: e => {
      if (!error) e.target.style.borderColor = 'var(--color-walnut)';
    },
    onBlur: e => {
      if (!error) e.target.style.borderColor = 'var(--color-champagne)';
    }
  }), error && /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: 'var(--font-body)',
      fontSize: '11px',
      color: '#9B2C2C'
    }
  }, error), hint && !error && /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: 'var(--font-body)',
      fontSize: '11px',
      color: 'var(--color-bronze)'
    }
  }, hint));
}
Object.assign(__ds_scope, { Textarea });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/forms/Textarea.jsx", error: String((e && e.message) || e) }); }

// components/navigation/Nav.jsx
try { (() => {
/**
 * FurnishIQ Nav — horizontal site navigation with logo, links, and CTA.
 */
function Nav({
  links = [],
  ctaLabel = 'Request a Consultation',
  onCtaClick,
  dark = false,
  transparent = false,
  logoSrc,
  logoAlt = 'FurnishIQ'
}) {
  const bgColor = transparent ? 'transparent' : dark ? 'var(--color-walnut-dark)' : 'var(--color-white)';
  const borderColor = transparent ? 'transparent' : dark ? 'rgba(214,194,168,0.15)' : 'var(--color-champagne)';
  const textColor = dark || transparent ? 'var(--color-champagne)' : 'var(--color-charcoal)';
  const linkHoverColor = dark ? 'var(--color-white)' : 'var(--color-walnut)';
  return /*#__PURE__*/React.createElement("nav", {
    style: {
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      padding: '0 var(--gutter)',
      height: 'var(--nav-height)',
      background: bgColor,
      borderBottom: `1px solid ${borderColor}`,
      position: 'relative',
      zIndex: 'var(--z-nav)'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'center',
      flexShrink: 0
    }
  }, logoSrc ? /*#__PURE__*/React.createElement("img", {
    src: logoSrc,
    alt: logoAlt,
    style: {
      height: '44px',
      width: 'auto',
      objectFit: 'contain'
    }
  }) : /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: 'var(--font-display)',
      fontSize: '22px',
      fontWeight: 'var(--weight-semibold)',
      letterSpacing: 'var(--tracking-wide)',
      color: dark ? 'var(--color-white)' : 'var(--color-walnut-dark)'
    }
  }, logoAlt)), /*#__PURE__*/React.createElement("ul", {
    style: {
      display: 'flex',
      alignItems: 'center',
      gap: '36px',
      listStyle: 'none',
      margin: 0,
      padding: 0
    }
  }, links.map((link, i) => /*#__PURE__*/React.createElement("li", {
    key: i
  }, /*#__PURE__*/React.createElement("a", {
    href: link.href || '#',
    style: {
      fontFamily: 'var(--font-body)',
      fontSize: '11px',
      fontWeight: 'var(--weight-medium)',
      letterSpacing: 'var(--tracking-wider)',
      textTransform: 'uppercase',
      color: link.active ? 'var(--color-walnut)' : textColor,
      textDecoration: 'none',
      borderBottom: link.active ? '1px solid var(--color-walnut)' : '1px solid transparent',
      paddingBottom: '2px',
      transition: 'color var(--transition-fast), border-color var(--transition-fast)'
    }
  }, link.label)))), /*#__PURE__*/React.createElement("button", {
    onClick: onCtaClick,
    style: {
      fontFamily: 'var(--font-body)',
      fontSize: '10px',
      fontWeight: 'var(--weight-semibold)',
      letterSpacing: 'var(--tracking-widest)',
      textTransform: 'uppercase',
      padding: '11px 28px',
      background: dark ? 'var(--color-champagne)' : 'var(--color-walnut)',
      color: dark ? 'var(--color-walnut-dark)' : 'var(--color-white)',
      border: 'none',
      borderRadius: 'var(--radius-none)',
      cursor: 'pointer',
      whiteSpace: 'nowrap',
      flexShrink: 0,
      transition: 'background var(--transition-base)'
    }
  }, ctaLabel));
}
Object.assign(__ds_scope, { Nav });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/navigation/Nav.jsx", error: String((e && e.message) || e) }); }

__ds_ns.Badge = __ds_scope.Badge;

__ds_ns.Button = __ds_scope.Button;

__ds_ns.Card = __ds_scope.Card;

__ds_ns.Divider = __ds_scope.Divider;

__ds_ns.Input = __ds_scope.Input;

__ds_ns.Select = __ds_scope.Select;

__ds_ns.Textarea = __ds_scope.Textarea;

__ds_ns.Nav = __ds_scope.Nav;

})();
