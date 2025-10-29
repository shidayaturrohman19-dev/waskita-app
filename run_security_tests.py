#!/usr/bin/env python3
"""
Security Test Runner
Comprehensive security testing and reporting script
"""

import os
import sys
import subprocess
import json
from datetime import datetime
from test_security import run_security_tests
from security_logger import get_security_stats

def check_security_dependencies():
    """Check if all security dependencies are available"""
    print("🔍 Checking security dependencies...")
    
    required_modules = [
        'flask',
        'bleach',
        'werkzeug',
        'flask_login'
    ]
    
    missing_modules = []
    for module in required_modules:
        try:
            __import__(module)
            print(f"✅ {module}")
        except ImportError:
            print(f"❌ {module} - MISSING")
            missing_modules.append(module)
    
    if missing_modules:
        print(f"\n⚠️  Missing dependencies: {', '.join(missing_modules)}")
        print("Install with: pip install " + " ".join(missing_modules))
        return False
    
    return True

def check_security_files():
    """Check if all security files exist"""
    print("\n🔍 Checking security implementation files...")
    
    required_files = [
        'security_utils.py',
        'security_logger.py',
        'security_middleware.py',
        'test_security.py'
    ]
    
    missing_files = []
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - MISSING")
            missing_files.append(file)
    
    if missing_files:
        print(f"\n⚠️  Missing files: {', '.join(missing_files)}")
        return False
    
    return True

def run_static_security_analysis():
    """Run static security analysis"""
    print("\n🔍 Running static security analysis...")
    
    # Check for common security issues in code
    security_issues = []
    
    # Check for hardcoded secrets
    print("Checking for hardcoded secrets...")
    try:
        result = subprocess.run(['grep', '-r', '-i', 'password.*=.*["\']', '.'], 
                              capture_output=True, text=True)
        if result.stdout:
            security_issues.append("Potential hardcoded passwords found")
    except:
        pass
    
    # Check for SQL injection vulnerabilities
    print("Checking for SQL injection vulnerabilities...")
    try:
        result = subprocess.run(['grep', '-r', 'execute.*%', '.'], 
                              capture_output=True, text=True)
        if result.stdout:
            security_issues.append("Potential SQL injection vulnerabilities found")
    except:
        pass
    
    if security_issues:
        print("⚠️  Security issues found:")
        for issue in security_issues:
            print(f"  - {issue}")
    else:
        print("✅ No obvious security issues found")
    
    return len(security_issues) == 0

def generate_security_report():
    """Generate comprehensive security report"""
    print("\n📊 Generating security report...")
    
    report = {
        'timestamp': datetime.utcnow().isoformat(),
        'security_stats': get_security_stats(),
        'test_results': {},
        'recommendations': []
    }
    
    # Add recommendations based on current state
    stats = report['security_stats']
    
    if stats['blocked_ips'] > 0:
        report['recommendations'].append(
            f"Review {stats['blocked_ips']} blocked IPs for potential threats"
        )
    
    if stats['total_events'] > 100:
        report['recommendations'].append(
            "High number of security events detected - review logs for patterns"
        )
    
    # Check log directory
    if os.path.exists('logs'):
        log_files = os.listdir('logs')
        report['log_files'] = log_files
        if len(log_files) > 10:
            report['recommendations'].append(
                "Consider implementing log rotation or cleanup"
            )
    
    # Save report
    report_file = f"security_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"📄 Security report saved to: {report_file}")
    return report

def main():
    """Main security testing function"""
    print("🛡️  WASKITA SECURITY TEST SUITE")
    print("=" * 50)
    
    # Check dependencies
    if not check_security_dependencies():
        print("\n❌ Dependency check failed!")
        return False
    
    # Check security files
    if not check_security_files():
        print("\n❌ Security files check failed!")
        return False
    
    # Run static analysis
    static_analysis_passed = run_static_security_analysis()
    
    # Run unit tests
    print("\n🧪 Running security unit tests...")
    unit_tests_passed = run_security_tests()
    
    # Generate report
    report = generate_security_report()
    
    # Print summary
    print("\n" + "=" * 50)
    print("🛡️  SECURITY TEST SUMMARY")
    print("=" * 50)
    
    print(f"Dependencies: {'✅ PASS' if True else '❌ FAIL'}")
    print(f"Security Files: {'✅ PASS' if True else '❌ FAIL'}")
    print(f"Static Analysis: {'✅ PASS' if static_analysis_passed else '⚠️  WARNINGS'}")
    print(f"Unit Tests: {'✅ PASS' if unit_tests_passed else '❌ FAIL'}")
    
    # Security recommendations
    if report['recommendations']:
        print(f"\n📋 Security Recommendations:")
        for i, rec in enumerate(report['recommendations'], 1):
            print(f"  {i}. {rec}")
    
    # Overall status
    overall_status = unit_tests_passed and static_analysis_passed
    print(f"\n🛡️  Overall Security Status: {'✅ SECURE' if overall_status else '⚠️  NEEDS ATTENTION'}")
    
    if not overall_status:
        print("\n⚠️  Please address the issues above before deploying to production!")
    
    return overall_status

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)